import logging
import time

from log import logger
from utils import helper as hp
from utils import parser 
from config import config

logger = logger.logger(__name__,logging.DEBUG)


if __name__ == '__main__':
    """
    Assupmtions:
        If value is not in the standard definition then discarded
    """
    # load standard definition 
    data_schema_json = hp.read_json(config.DATA_SCHEMA_PATH)

    # load error code
    error_code = hp.read_json(config.ERROR_CODE_PATH)

    # get sections from the data schema definition
    section_list = hp.get_sections_list(data_schema_json)
    logger.info(f'Available section values from the standard definition: {section_list}')

    start_time = time.time()

    report_list_of_list, summary_list = parser.file_parser(input_path=config.INPUT_PATH,
                                                            data_schema_json=data_schema_json,
                                                            section_list=section_list,
                                                            error_code=error_code) 


    # save report as csv file
    result_csv = hp.save_to_csv(report=report_list_of_list,
                                report_path=config.REPORT_PATH)
    logger.debug(f'Write csv file to disk: {result_csv}')

    # save summary as text file
    result_txt = hp.save_to_txt(summary=summary_list,
                                    dest_path=config.SUMMARY_PATH)
    logger.debug(f'Write text file to disk: {result_txt}')


    logger.info(f'Program execution time: {time.time() -  start_time} secs')


