import logging
import json

import pandas as pd

from config import config
from log import logger

logger = logger.logger(__name__,logging.DEBUG)

# function to read the json file
def read_json(file_path:str):
    """
    Function to read and return json file

    Args:
        file_path: json file path

    Returns
        json object
    """
    
    try:
        # read the json file
        with open(file_path,'r') as json_file:
            json_file = json.load(json_file)
            return json_file
    except:
        logger.exception('Error!! Json file not found')


# function to get the list of section from the json data schema
def get_sections_list(json_file:list):
    """
    Function to get the list of sections from the data schema

    Args:
        json_file: data schema in the form of json file

    Returns:
        sections list
    """

    # empty section list
    section_list = []

    try:
        for json_object in json_file:
            #print(section['sub_sections'])
            for key,value in json_object.items():
                #check if the value is the key
                if type(json_object[key]) == type('check_string_type'):
                    section_list.append(json_object[key])

    except:
        logger.exception('Error!! Json object None')

    return section_list

# function to return data type and max_length based on 
# section_key and sub_section_key
def get_validation_criteria(json_file,section,sub_section):
    """
    Function to return validation criteria for the sub_section i.e. 
    data type and max_length allowed

    Args:
        json_file: json file consisting the schema
        section: section value related to the json
        sub_section: sub_section value related to section

    Returns: 
        tuple: (data_type, max_length) if success else (None, error message)
    """

    for json_object in json_file:
        for key,value in json_object.items():            
            if value == section:
                for value in json_object['sub_sections']:
                    if value['key'] == sub_section:
                        return value['data_type'],value['max_length']
            
                # if it doesn't find the value then
                return None,'value not found!!'



def summary_msg_formatter(msg_format: str ,segment_name:str ,field_num: int,
                            validation: tuple=None):
    """
    Function to return summary message

    Args:
        msg_format: message format for the summary message
        segment_name: name of the segment
        field_num: field number related to segment name 
        validation: validation tuple from standard definition for field_num from segment_name

    Returns:
        Formatted summary message
    """

    try:
        msg_format = msg_format.replace('LX',segment_name).replace('Y',str(field_num))
    except:
        logger.exception('Error!! string value replacement in given messag format')

    if validation ==  None:
        return msg_format

    else:
        try:
            msg_format= msg_format.format(data_type=validation[0],max_length=validation[1])
            return msg_format
        except:
            logger.exception('Error!! string format in validation section')


def save_to_csv(report:list):
    """
    Function to save the report as csv file into destination directory

    Args:
        report: report data as list of list
    """

    df = pd.DataFrame(report,columns=config.REPORT_COLMNS)

    logger.info(f'Columns for the data: {df.columns}')

    try:
        logger.info(f'Report destination: {config.REPORT_PATH}')
        df.to_csv(config.REPORT_PATH,index=False)

    except:
        logger.exception('Error!! cannot write the file')


def save_to_txt(summary:list):
    """
    Function to save the summary as text file into destination directory

    Args:
        summary: summary data as list
    """

    try:
        logger.info(f'Summary destination: {config.SUMMARY_PATH}')
        with open(config.SUMMARY_PATH, 'w') as file:
            for row in summary:
                file.write(row+'\n')

    except:
        logger.exception('Error!! cannot write the file')