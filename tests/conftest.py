import pytest
import pandas as pd

import os
from pathlib import Path
import logging

from log import logger
from config import config
from utils import helper as hp
from utils import parser

logger = logger.logger(__name__,logging.DEBUG)

# root package

PACKAGE_ROOT = Path().resolve()

logger.info(f'Root path: {PACKAGE_ROOT}')

PACKAGE_ROOT_DATA = os.path.join(PACKAGE_ROOT,'data')

logger.info(f'Data path: {PACKAGE_ROOT_DATA}')

"""
Test Objective:

1. Test file and its path in config file
2. Unit test for the helper functions
3. Unit test for parser functions

"""

@pytest.fixture()
def data_for_test():

    test_data = config.TEST_DATA_PATH

    yield test_data


@pytest.fixture()
def standard_definition():

    data_schema = hp.read_json(file_path=config.DATA_SCHEMA_PATH)

    yield data_schema


@pytest.fixture()
def error_definition():

    error_code = hp.read_json(file_path= config.ERROR_CODE_PATH)

    yield error_code

@pytest.fixture()
def section_list():

    # list consisting the name of section in the data schema
    section_list = ['L1', 'L2', 'L3', 'L4']

    yield section_list


@pytest.fixture()
def section_dict():

    # dictionary consisting sections as key and subsection array as value
    section_dict = { 'L1': ['L11','L12','L13'],
                          'L2': ['L21','L22','L23'],
                          'L3': ['L31','L33'],
                          'L4': ['L41','L42']}

    yield section_dict


@pytest.fixture()
def summary_report(standard_definition,section_list,
                        error_definition):
    """ Yields report and summary list for test file """

    report,summary = parser.file_parser(input_path=config.TEST_DATA_PATH,
                                            data_schema_json=standard_definition,
                                            section_list=section_list,
                                            error_code=error_definition)

    yield report, summary


@pytest.fixture()
def input_files():
    """ input files name"""

    stand_definition = 'standard_definition.json'
    input_file = 'input_file.txt'
    error_file = 'error_codes.json'

    yield stand_definition, input_file, error_file

@pytest.fixture()
def output_files():
    """ output files name """

    report_file = 'report.csv'
    summary_file =  'summary.txt'

    yield report_file, summary_file


@pytest.fixture()
def report_cols():
    """ Report file columns """

    report_cols = REPORT_COLMNS = ["Section","Sub-Section",
                            "Given DataType",
                        "Expected DataType","Given Length",
                        "Expected MaxLength","Error Code"]


    yield report_cols


@pytest.fixture()
def input_file_paths(input_files):
    """ input files path"""

    stand_definition, input_file, error_file = input_files

    stand_def_path = os.path.join(PACKAGE_ROOT_DATA,stand_definition)
    input_path = os.path.join(PACKAGE_ROOT_DATA,input_file)
    error_code_path = os.path.join(PACKAGE_ROOT_DATA,error_file)

    yield stand_def_path,input_path,error_code_path


@pytest.fixture()
def output_file_paths(output_files):
    """ input files path"""

    report_file, summary_file = output_files
    OUTPUT_DIR = 'parsed'

    report_path = os.path.join(PACKAGE_ROOT_DATA,OUTPUT_DIR,report_file)
    summary_path = os.path.join(PACKAGE_ROOT_DATA,OUTPUT_DIR,summary_file)

    yield report_path,summary_path





