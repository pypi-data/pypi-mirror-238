"""stdfconvert

Usage:
  stdfconvert end2end <inglob> <outdir> <format>
  stdfconvert pickle2format <outfile> <format>
  stdfconvert stdf2pickle


"""
import os
import rich
import rich.progress
import subprocess
from rich.progress import Progress
import time
import glob
import pathlib
import sys
import ams_rw_stdf
import collections
import pickle
import threading
import queue
from docopt import docopt
import toml
import sys
import ams_rw_stdf
import collections
import pickle
import threading
import queue
import shutil
from rich.console import Console
error_console = Console(stderr=True, style="bold red")


def convert_list_of_files(fileGlob, outdir, format="parquet"):
    stdf_to_pickle_cmd   = f"{sys.executable} -m  ams_rw_stdf.convert stdf2pickle"
    typical7zLocations = ["7z", "7Z", f"{os.getenv('ProgramFiles(x86)')}/7-Zip/7z.exe", f"{os.getenv('ProgramFiles')}/7-Zip/7z.exe"]
    sevenZLocations = [shutil.which(item) for item in typical7zLocations]
    sevenZLocations = [item for item in sevenZLocations if item is not None]
    if sevenZLocations:
        sevenZ = sevenZLocations[0]
        gzip_handler = f"\"{sevenZ}\" e -tgzip -si -so"
        bzip_handler = f"\"{sevenZ}\" e -tbzip -si -so"
        xz_handler = f"\"{sevenZ}\" e -txz -si -so"
    else:
        gzip_handler         = shutil.which("zcat")
        bzip_handler         = shutil.which("bzcat")
        xz_handler           = shutil.which("unxz")
    
    for configfile in ["/etc/stdf-tamer.toml", pathlib.Path(os.path.expanduser("~")) / ".config/stdf-tamer.toml"]:
        try:
            config = toml.load(configfile)
            if "stdf_to_pickle_cmd" in config["converter"]:
                stdf_to_pickle_cmd   = config["converter"]["stdf_to_pickle_cmd"]
            if "zcat" in config["converter"]:
                 gzip_handler = config["converter"]["zcat"]
            if "bzcat" in config["converter"]:
                 bzip_handler = config["converter"]["bzcat"]
            if "unxz" in config["converter"]:
                 xz_handler = config["converter"]["unxz"]
        except:
            pass

    picke_to_parquet_cmd = f"{sys.executable} -m  ams_rw_stdf.convert pickle2format"

    if not xz_handler:
        error_console.print("Unable to find xz decompression tool. Please install/configure 7z/unxz")
    if not bzip_handler:
        error_console.print("Unable to find bzip2 decompression tool. Please install/configure 7z/bzcat")
    if not gzip_handler:
        error_console.print("Unable to find gz decompression tool. Please install/configure 7z/zcat")

    flist = list(glob.glob(fileGlob))
    if not flist:
        error_console.print("No files to convert")
    with Progress(rich.progress.TextColumn("[progress.description][red]{task.description}"),
                  rich.progress.TimeElapsedColumn(),
                  rich.progress.DownloadColumn(), rich.progress.BarColumn(),
                  rich.progress.TransferSpeedColumn(),
                  rich.progress.TimeRemainingColumn ()) as progress:

        def get_file_size(item):
            return os.stat(item).st_size

        def _worker(outdir, flist):
            outdir = pathlib.Path(outdir).resolve()
            flist = list(reversed(sorted(flist, key=get_file_size)))
            for fname in flist:
                file = open(fname, "rb")
                fnameShort = pathlib.Path(fname).name
                if fname.endswith(".stdf.xz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    yield (file, f"{xz_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} {ofname}.{format} {format}",)
                elif fname.endswith(".stdf.gz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    yield (file, f"{gzip_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} {ofname}.{format} {format}",)
                elif fname.endswith(".stdf") or fname.endswith(".std"):
                    ofname = outdir / f"{fnameShort[:-5]}"
                    yield (file, f"{stdf_to_pickle_cmd} | {picke_to_parquet_cmd} {ofname}.{format} {format}",)
                elif fname.endswith(".stdf.bz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    yield (file, f"{bzip_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} {ofname}.{format} {format}",)

        items = list(_worker(outdir, flist))
        totSize = sum(os.stat(item).st_size for item in flist)
        task = progress.add_task("converting", total=totSize)
        processes2run = items
        fs = [item[0] for item in items]
        running_processes = []
        max_running_conversions = os.cpu_count()/2

        while running_processes or processes2run:
            while len(running_processes) < max_running_conversions and processes2run:
                (file, cmd,)  = processes2run.pop()
                running_processes.append(subprocess.Popen(cmd, shell=True, stdin=file))
            progress.update(task, completed=sum(item.tell() for item in fs))
            time.sleep(0.001)
            running_processes = [item for item in running_processes if item.poll() is None]


def pickle2X(options):
    try:
        import polars as pl

        schema = [('Test_Nr', pl.UInt32),
                  ('Test_Name', pl.Utf8),
                  ('ULim', pl.Float32),
                  ('LLim', pl.Float32),
                  ('res', pl.Float32),]
    except ImportError as e:
        print('writing parquet failed due to missing dependencies', file=sys.stderr)
        return
    def worker():
        try:
            while True:
                yield pickle.load(sys.stdin.buffer)
        except:
            pass
    worker = worker()
    (lot_id, test_cod, operator, start_t, ) = next(worker)

    def worker_():
        for (data, part_id, part_txt, head, site) in worker:
            df = pl.DataFrame(data, schema=schema)
            df = df.with_columns(pl.lit(part_id).cast(pl.Utf8).alias("part_id"),
                                 pl.lit(part_txt).cast(pl.Utf8).alias("part_txt"),
                                 pl.lit(head).cast(pl.Utf8).alias("head"),
                                 pl.lit(site).cast(pl.Utf8).alias("site"))
            yield df

    df = pl.concat(worker_())
    df = df.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("TEST_COD"),
                         pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                         pl.lit(operator).cast(pl.Categorical).alias("operator"),
                         pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                         pl.col("Test_Name").cast(pl.Categorical).alias("Test_Name"),
                         pl.col("part_id").cast(pl.Categorical).alias("part_id"),
                         pl.col("part_txt").cast(pl.Categorical).alias("part_txt"),)
    if options["<format>"] == "xlsx":
        df.write_excel(options["<outfile>"])
    elif options["<format>"] == "ipc" or options["<format>"] == "feather":
        df.write_ipc(options["<outfile>"])
    else:
        df.write_parquet(options["<outfile>"])


def _worker(q):
    b = sys.stdout.buffer
    while True:
            b.write(pickle.dumps(q.get()))
            q.task_done()


def stdf2pickle():
    data =  collections.defaultdict(lambda : [])
    q = queue.Queue()
    threading.Thread(target=_worker, daemon=True, args=(q,)).start()

    try:
        for c in ams_rw_stdf.records_no_length_simplified():
            type_and_subtyp = (c.REC_TYP, c.REC_SUB,)
            PL = c.PL
            if type_and_subtyp == (15, 10,):
                key = (PL.HEAD_NUM,  PL.SITE_NUM,)
                data[key].append((PL.TEST_NUM, PL.TEST_TXT, PL.HI_LIMIT, PL.LO_LIMIT, PL.RESULT,))
            elif type_and_subtyp == (5, 20,):
                key = (PL.HEAD_NUM, PL.SITE_NUM)
                res = (data[key], PL.PART_ID, PL.PART_TXT, PL.SITE_NUM, PL.HEAD_NUM,)
                q.put(res)
                data[key] = []
            elif type_and_subtyp == (1, 10,):
                test_cod = PL.TEST_COD
                lot_id   = PL.LOT_ID
                operator = PL.OPER_NAM
                start_t = PL.START_T
                q.put((lot_id, test_cod, operator, start_t, ))
            elif type_and_subtyp == (1, 20,):
                q.join()
                exit(0)
    except Exception as e:
        q.join()
        sys.exit(f"unexpected end of stdf (exception: {e})")


def main():
    options = docopt(__doc__)
    if options["stdf2pickle"]:
        stdf2pickle()
    elif options["pickle2format"]:
        pickle2X(options)
    elif options["end2end"]:
        convert_list_of_files(options["<inglob>"], options["<outdir>"], options["<format>"])


if __name__ == "__main__":
    main()
