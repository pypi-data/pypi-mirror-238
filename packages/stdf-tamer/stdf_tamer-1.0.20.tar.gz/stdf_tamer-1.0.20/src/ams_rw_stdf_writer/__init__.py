import itertools
import re
import ams_rw_stdf
import socket
import os
import time
import bz2
import gzip
import polars as pl
import shutil
import collections
from datetime import datetime
from datetime import timezone
import pathlib
import ams_rw_stdf._ams_rw_stdf_writer_state as state
import tempfile
from logging import warning
from logging import info
from logging import error

_tmpdirname = pathlib.Path(tempfile.mkdtemp())

def _write2streams(stream, data):
    stream.ostream.write(data)
    try:
        stream.last_part_stream.write(data)
    except:
       pass


from ams_rw_stdf._opener_collection import _opener


def load_limit_file(path_of_limit_file):
    """
    Loads a limit file and resets all collected information on a sample.
    """
    schema = [('Test number', pl.UInt32), 
              ('Test name', pl.Utf8), 
              ('Min', pl.Float32), 
              ('Max', pl.Float32), 
              ("Prefix", pl.Utf8), 
              ("Unit", pl.Utf8), 
              ("Bin", pl.Int16)]
    limits = pl.read_excel(path_of_limit_file, sheet_id=0)
    limits = (i[['Test number', 'Test name', 'Min', 'Max', 'Prefix', 'Unit', 'Bin']] for i in limits.values())
    limits = (item.with_columns(*[pl.col(item[0]).cast(item[1]) for item in schema]) for item in limits)
    limits = pl.concat(limits)
    limits = limits.filter(~pl.all_horizontal(pl.all().is_null()))
    state.limit_db = limits
    duplicatedTestEntries = (limits.groupby(['Test number', 'Test name']).count().filter(pl.col("count")>1).select(["Test number", "Test name"]))
    duplicated_test_names = (limits.groupby('Test name').count().filter(pl.col("count")>1).select(["Test name"]))['Test name']
    duplicated_test_numbers = (limits.groupby('Test number').count().filter(pl.col("count")>1))['Test number']
    assert duplicatedTestEntries.is_empty(), f"duplicated test limit entries: {', '.join(str(item[0]) +': ' + str(item[1]) for item in sorted(duplicatedTestEntries.rows()))}"
    assert duplicated_test_numbers.is_empty(), f"duplicated test numbers: {'; '.join(str(i) for i in sorted(duplicated_test_numbers.to_list()))}"
    assert duplicated_test_names.is_empty(), f"duplicated test names: {'; '.join(duplicated_test_names)}"
    state.limit_db = state.limit_db.with_columns(pl.lit(0).alias("usage_count"), pl.lit(0).alias("limit_check_order"))
    state.limit_check_order_information = 0

def start_stdf_file(stdf_file_name, part_type, lot_id, operator, test_setup_id, test_cod, tp_version, retestbins=""):
    """
    Creates a handle to use for stdf file writing.

    If the file does not exist, a new one is started. If a file does exist, data has already been written to it, but not from 
    the sampe process as the current one, it is an error.

    If this function is called multiple times within the scope of a process, subsequent calls return fresh handles, which can be used.

    - retestbins Empty string means first test, otherwise notes the bins which get retested
    """
    global _tmpdirname
    ofilePath = pathlib.Path(stdf_file_name)
    real_f_name = _tmpdirname / (ofilePath.name)
    last_part = _tmpdirname / ("last_part_" + ofilePath.stem + ".stdf")

    if os.devnull in {ofilePath.name, ofilePath.absolute()}:
        _last_part_stream = open(os.devnull, "wb")
    else:
        _last_part_stream = _opener[last_part.suffix](last_part, "wb")

    stream = open(real_f_name, "a+b")
    utctimestamp = int(datetime.now(timezone.utc).timestamp())
    retestFlagsFromRetestBins = collections.defaultdict(lambda: "T", {"": "F"})
    preamble = [{'REC_LEN': 2,
                 'REC_TYP': 0,
                 'REC_SUB': 10,
                 'PL': {'CPU_TYPE': b'\x02', 'STDF_VER': b'\x04'}},
                {'REC_LEN': 254,
                 'REC_TYP': 1,
                 'REC_SUB': 10,
                 'PL': {'SETUP_T': utctimestamp,
                        'START_T': utctimestamp,
                        'STAT_NUM': 1,
                        'MODE_COD': "1",
                        'RTST_COD': "N",
                        'PROT_COD': " ",
                        'BURN_TIM': 65535,
                        'CMOD_COD': " ",
                        'LOT_ID': lot_id,
                        'PART_TYP': part_type,
                        'NODE_NAM': socket.gethostname(),
                        'TSTR_TYP': 'PXI',
                        'JOB_NAM': '',
                        'JOB_REV': f"{tp_version};;",
                        'SBLOT_ID': '1',
                        'OPER_NAM': operator,
                        'EXEC_TYP': '',
                        'EXEC_VER': '',
                        'TEST_COD': test_cod,
                        'TST_TEMP': '25',
                        'USER_TXT': f'P - Production;T - Final Test;1;F;{retestFlagsFromRetestBins[retestbins]};{retestbins};',
                        'AUX_FILE': '',
                        'PKG_TYP': '',
                        'FAMLY_ID': 'ENGINEERINGTESTDATAINTERFACE;;;;1',
                        'DATE_COD': '',
                        'FACIL_ID': '1100',
                        'FLOOR_ID': '',
                        'PROC_ID': '',
                        'OPER_FRQ': '',
                        'SPEC_NAM': '',
                        'SPEC_VER': '',
                        'FLOW_ID': 'MAIN_FLOW',
                        'SETUP_ID': test_setup_id,
                        'DSGN_REV': '',
                        'ENG_ID': '',
                        'ROM_COD': '',
                        'SERL_NUM': '',
                        'SUPR_NAM': ''}}]
    if os.stat(real_f_name).st_size == 0:
        state.bin_counter = collections.defaultdict(lambda: 0)
        state._meas_run_num = 0
        for item in preamble:
            stream.write(ams_rw_stdf.RECORD.build(item))
    
    for item in preamble:
        _last_part_stream.write(ams_rw_stdf.RECORD.build(item))

    state._meas_run_num = state._meas_run_num + 1
    
    assert state.bin_counter is not None, "please collect and move away results before starting over"
    assert state._meas_run_num is not None, "please collect and move away results before starting over"
    return collections.namedtuple("stdf_hanlde", ["ostream", "filename", "last_part_stream"])(stream, ofilePath, _last_part_stream)

def start_sample(stream):
    """
    Adds an PIR record to the stdf.
    """
    state._this_test_running_data = {"NUM_TEST": 0, "FAILS": 0, "PASSES": 0, "start_t": int(datetime.now(timezone.utc).timestamp()), "BIN": 1}
    data = {'REC_LEN': 2, 'REC_TYP': 5, 'REC_SUB': 10, 'PL': {'HEAD_NUM': 1, 'SITE_NUM': 1}}
    _write2streams(stream, ams_rw_stdf.RECORD.build(data))

_search_for_bin_num = c = re.compile("/[0-9]*/")
def _get_bin_from_test_name(testname):
    try:
        all_matches = _search_for_bin_num.findall(testname)
        num_of_bin_nums = len(all_matches)
        if num_of_bin_nums != 1:
            warning(f"There should be exactly one fail bin number in every test name ({testname} has {num_of_bin_nums})")
        return int(all_matches[0].replace("/", ""))
    except:
        warning(f"{testname}: does not have a fail bin number")
        return 7

def _low_level_test_value(stream, test_num, testname, passed_value, lo_lim, hi_lim, unit, prefix, OPT_FLAG):
    if testname.strip() != testname:
        warning(f"'{testname}': has whitespaces which are confusing!")
    assert state._this_test_running_data is not  None, "outside of part segment!"
    unit = str(unit)
    prefix = str(prefix)
    test_num = int(test_num)

    _prefixes = {str(key): value for key, value in {None: 0, "nan": 0, "": 0, "1": 0, 1:0, "m": 3, "u": 6, "n": 9, "p": 12}.items()}
    scaling_factor = 1
    if prefix and prefix in _prefixes:
        scaling_factor = 10 ** _prefixes[str(prefix)]


    value = passed_value * scaling_factor

    not_too_low = (lo_lim <= value)
    not_too_high = (hi_lim >= value)
    result = not_too_low & not_too_high
    flag = {True: 0x00, False: 0x80}[result]

    data = {'REC_LEN': 77,
            'REC_TYP': 15,
            'REC_SUB': 10,
            'PL': {'TEST_NUM': test_num,
                   'HEAD_NUM': 1,
                   'SITE_NUM': 1,
                   'TEST_FLG': flag,
                   'PARM_FLG': 0,
                   'RESULT':   passed_value,
                   'TEST_TXT': testname,
                   'ALARM_ID': '',
                   'OPT_FLAG': OPT_FLAG,
                   'RES_SCAL': _prefixes[prefix],
                   'LLM_SCAL': _prefixes[prefix],
                   'HLM_SCAL': _prefixes[prefix],
                   'LO_LIMIT': lo_lim / scaling_factor,
                   'HI_LIMIT': hi_lim / scaling_factor,
                   'UNITS': unit,
                   'C_RESFMT': '%9.3f',
                   'C_LLMFMT': '%9.3f',
                   'C_HLMFMT': '%9.3f',
                   'LO_SPEC': 0.0,
                   'HI_SPEC': 0.0}}

    _write2streams(stream, ams_rw_stdf.RECORD.build(data))
    return result, (lo_lim, value, hi_lim,)



def test_value_between(stream, test_num, testname, value):
    """
    Checks a limit, keeps track of which limits have been checked so that duplicates and missing checks *could* be detected.
    
    Adds an PTR reckord to the stdf.
    """
    key = (int(test_num), testname,)
    selector = (pl.col("Test number")==int(test_num)) & (pl.col("Test name")==testname)

    entry = state.limit_db.filter((pl.col("Test number")==int(test_num)) & (pl.col("Test name")==testname))
    
    assert len(entry) > 0, f"""no test limits for "{key[0]} {key[1]}" in the limit file"""
    assert len(entry) <= 1, f"""more than one limit for "{key[0]} {key[1]}" in the limit file"""

    assert state._this_test_running_data is not  None, "outside of part segment!"

    lo_lim, hi_lim, prefix, unit = entry[["Min", "Max", "Prefix",  "Unit"]].rows()[0]
    
    result, (lo_lim, value, hi_lim,) = _low_level_test_value(stream, test_num, testname, value, lo_lim, hi_lim, unit, prefix, 0x0e)
    state.limit_db = state.limit_db.with_columns(pl.when(selector).then((pl.col("usage_count")+1)).otherwise(pl.col("usage_count")).alias("usage_count"))
    state.limit_check_order_information += 1
    state.limit_db = state.limit_db.with_columns(pl.when(selector).then((pl.lit(state.limit_check_order_information).alias("limit_check_order"))))
    state._this_test_running_data["NUM_TEST"] += 1

    #key is global pass, local pass status
    next_bins = {(True, True): 1, 
                 (True, False): _get_bin_from_test_name(testname),
                 (False, False): state._this_test_running_data["BIN"],
                 (False, True): state._this_test_running_data["BIN"]}
    
    state._this_test_running_data["BIN"]    = next_bins[(state._this_test_running_data["FAILS"] == 0, result)]
    state._this_test_running_data["FAILS"] += bool(False == result)

    counts_as = {True: "PASSES", False: "FAILS"}[result]
    state._this_test_running_data[counts_as] += 1

    assert result, f"{test_num} {testname} failed: outside of limits {lo_lim} <= {value} <= {hi_lim}"
    info(f"{test_num}, {testname}: {lo_lim} <= {value} <= {hi_lim}")


def store_information_value_in_stdf(stream, test_num, testname, value, unit="#", prefix=""):
    """
    Stores inforamtion value. All bets are of.
    
    Adds an PTR reckord to the stdf.
    """
    assert "_info/" in testname, "information parameters need to have '_info/' in their name"
    _low_level_test_value(stream, test_num, testname, value, float("-inf"), float("inf"), unit, prefix, 0xce)
    

def get_number_of_unchecked_limits():
    """Returns the number of limits which have not been checked since the limit file was loaded."""
    return len(state.limit_db.filter(pl.col("usage_count")==0))


def get_number_of_limits_checked_more_than_once():
    """Returns the number of limits which have been checked more than once since the limit file was loaded."""
    return len(state.limit_db.filter(pl.col("usage_count")>1))

def check_that_every_limit_is_checked_once():
    """Also writes a excel sheet which consists of some extra information."""
    state.limit_db.write_excel("checks.xlsx")
    assert get_number_of_unchecked_limits() == 0, "some limits where not checked"
    assert get_number_of_limits_checked_more_than_once() == 0, "not all limits where checked exactly once"

def proportion_of_tests_complete():
    """Returns proportion of competed tests, regardless of pass or fail. 
    
    This is intended to be used with progress indicators."""
    numLimits = len(state.limit_db)
    return (numLimits - get_number_of_unchecked_limits()) / numLimits

def _finish_sample(stream, id):
    bin_num = state._this_test_running_data["BIN"]
    state.bin_counter[bin_num] += 1
    data = {'REC_LEN': 34,
            'REC_TYP': 5,
            'REC_SUB': 20,
            'PL': {'HEAD_NUM': 1,
                   'SITE_NUM': 1,
                   'PART_FLG': 0,
                   'NUM_TEST': state._this_test_running_data["NUM_TEST"],
                   'HARD_BIN': bin_num, #here we could do a special bin 100 if we would want to
                   'SOFT_BIN': bin_num,
                   'X_COORD': -32768,
                   'Y_COORD': -32768,
                   'TEST_T': int(1000*(time.time() - state._this_test_running_data["start_t"])),
                   'PART_ID': f"{state._meas_run_num}",
                   'PART_TXT': f"{state._run_mode};{id};",
                   'PART_FIX': ''}}
    _write2streams(stream, ams_rw_stdf.RECORD.build(data))
    state._this_test_running_data = None


def _finish_stdf_file(singleStream):
    PFs = collections.defaultdict(lambda: "F", {1: "P"})
    bin_sequence = ([{'REC_LEN': 10,
                       'REC_TYP': 1,
                       'REC_SUB': 40,
                       'PL': {'HEAD_NUM': 1,
                              'SITE_NUM': 1,
                              'HBIN_NUM': binNr,
                              'HBIN_CNT': binCnt,
                              'HBIN_PF':  PFs[binNr],
                              "HBIN_NAM": f"HBIN_{binNr}"}},
                        {'REC_LEN': 10,
                         'REC_TYP': 1,
                         'REC_SUB': 50,
                         'PL': {'HEAD_NUM': 1,
                                'SITE_NUM': 1,
                                'SBIN_NUM': binNr,
                                'SBIN_CNT': binCnt,
                                'SBIN_PF':  PFs[binNr],
                                "SBIN_NAM": f"SBIN_{binNr}"}}]
                       for binNr, binCnt in state.bin_counter.items())

    for data in itertools.chain.from_iterable(bin_sequence):
        singleStream.write(ams_rw_stdf.RECORD.build(data))
    singleStream.write(ams_rw_stdf.RECORD.build({'REC_LEN': 10,
                                                 'REC_TYP': 1,
                                                 'REC_SUB': 20,
                                                 'PL': {'FINISH_T': int(datetime.now(timezone.utc).timestamp()),
                                                        'DISP_COD': " ",
                                                        'USR_DESC': '',
                                                        'EXC_DESC': ''}}))


def finish_sample(stream, id):
    """Writes out binning information and PRR to the stdf file"""
    bin_num = state._this_test_running_data["BIN"]
    ofilePath = pathlib.Path(stream.ostream.name)
    if os.devnull not in {ofilePath.name, ofilePath.absolute()}:
        _finish_sample(stream, id)
        stream.ostream.flush()
        with tempfile.TemporaryDirectory() as tmpdirname:
            intermediate_file_name = pathlib.Path(tmpdirname) / pathlib.Path(stream.ostream.name).name
            stream.ostream.seek(0, 0)
            ostream = _opener[intermediate_file_name.suffix](intermediate_file_name, "wb")
            shutil.copyfileobj(stream.ostream, ostream)
            _finish_stdf_file(ostream)
            ostream.close()
            _finish_stdf_file(stream.last_part_stream)
            last_part_name = stream.last_part_stream.name
            stream.last_part_stream.close()
            last_part_target = pathlib.Path(stream.filename).parent / ("last_part_" + stream.filename.name)
            os.replace(intermediate_file_name, stream.filename)
            os.replace(last_part_name, last_part_target)
    return bin_num
