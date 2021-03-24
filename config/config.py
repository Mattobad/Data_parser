import os
from pathlib import Path


# root package
PACKAGE_ROOT =Path('data').resolve()


"""
FILE NAMES
"""
DATA_SCHEMA_FILE = 'standard_definition.json'

INPUT_FILE = 'input_file.txt'

ERROR_CODE_FILE = 'error_codes.json'

"""
FILE PATHS
""" 

DATA_SCHEMA_PATH = os.path.join(PACKAGE_ROOT,DATA_SCHEMA_FILE)

INPUT_PATH = os.path.join(PACKAGE_ROOT,INPUT_FILE)

ERROR_CODE_PATH = os.path.join(PACKAGE_ROOT,ERROR_CODE_FILE)


"""
OUTPUT FILE
"""
REPORT_FILE = 'report.csv'

SUMMARY_FILE = 'summary.txt'


"""
OUPUT PATH
"""
OUTPUT_DIR = 'parsed'

OUTPUT_DIR_PATH = os.path.join(PACKAGE_ROOT,OUTPUT_DIR)

REPORT_PATH = os.path.join(OUTPUT_DIR_PATH,REPORT_FILE)

SUMMARY_PATH = os.path.join(OUTPUT_DIR_PATH,SUMMARY_FILE)


# columns for report file

REPORT_COLMNS = ["Section","Sub-Section","Given DataType",
                        "Expected DataType","Given Length",
                        "Expected MaxLength","Error Code"]








