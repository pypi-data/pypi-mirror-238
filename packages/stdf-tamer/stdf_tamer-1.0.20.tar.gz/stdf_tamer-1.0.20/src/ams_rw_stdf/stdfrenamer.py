"""Renames stdf based on MIR conntent

This has the full power of python fstring formating...


Usage:
  stdfrenamer <stdf_file_name_in>  --format="{MIR_LOT_ID}_{MIR_PART_TYP}.stdf"

Options:
  -h --help               Show this screen.
  --format="fmt string"   A python fstring type format stirng. The modules, datetime, zoneinfo, uuid, random are available
  stdf_file_name_in       python globs are allowed to select multiple input files (https://docs.python.org/3/library/glob.html)

"""


import ams_rw_stdf
from docopt import docopt
from ams_rw_stdf._opener_collection import _opener
import pathlib
import shutil
import glob
import datetime
import zoneinfo
import uuid
import random

def worker(si, fmt):
    ftype = pathlib.Path(si).suffix
    dest = None
    globals_for_eval = {}
    with _opener[ftype](si, "rb") as f:
        parser = ams_rw_stdf.compileable_RECORD.compile()
        while True:
             b = ams_rw_stdf.get_record_bytes(f)
             c = parser.parse(b)
             if c.REC_TYP == 1 and c.REC_SUB == 10:
                globals_for_eval = globals_for_eval | {f"MIR_{key}": value for key, value in dict(c.PL).items()}
                break
    dest = pathlib.Path(eval(fmt, globals_for_eval)).expanduser().absolute()
    dest.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copy(si, dest)
    

def main():
    arguments = docopt(__doc__)
    si = arguments["<stdf_file_name_in>"]
    fmt = arguments["--format"]
    fmt = f'f"{fmt}"'
    for item in glob.glob(si):
        worker(item, fmt)
        

if __name__ == '__main__':
    main()

