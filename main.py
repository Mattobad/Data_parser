import logging
import time

from log import logger
from utils import helper as hp
from utils import parser 
from config import config

logger = logger.logger(__name__,logging.DEBUG)


def init_parser() -> None:
    """
    Funtion to start the parsing of the input file

    Returns:
        None
    """

    report_list_of_list, summary_list = parser.file_parser(input_path=config.INPUT_PATH) 

    #save report as csv file
    result_csv = hp.save_to_csv(report=report_list_of_list,
                                report_path=config.REPORT_PATH)
    logger.debug(f'Write csv file to disk: {result_csv}')
    
    # save summary as text file
    result_txt = hp.save_to_txt(summary=summary_list,
                                    dest_path=config.SUMMARY_PATH)
    logger.debug(f'Write text file to disk: {result_txt}')


if __name__ == '__main__':
    """
    Assupmtions:
        If value is not in the standard definition then discarded
    """

    start_time = time.time()
    logger.info('File parsing started!!')
    init_parser()
    logger.info(f'Program execution time: {time.time() -  start_time} secs')


