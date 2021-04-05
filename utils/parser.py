import logging

from config import config
from log import logger
from utils import helper as hp


logger = logger.logger(__name__,logging.DEBUG)


def file_parser(input_path:str) -> tuple:
    """
    Function to parse the text file

    Args:
        input_path: file path
    Returns:
        tuple: report file as list of list and summary file as list
    """

    # two list one for summary and one for report
    data_summary_list = []

    #list of list to create report
    data_report_list = []

     # load standard definition 
    data_schema_json = hp.read_json(config.DATA_SCHEMA_PATH)
    # load error code
    error_code = hp.read_json(config.ERROR_CODE_PATH)
    # get sections from the data schema definition
    section_list = hp.get_sections_list(data_schema_json)
    logger.info(f'Available section values from the standard definition: {section_list}')

    # read the file
    with open(input_path,'r') as txt_file:
        # track the row number
        row_index = 1
        for line in txt_file:
            logger.info(f'Row number: {row_index}')

            row_report,row_summary = row_parser(row_data = line, data_schema_json =data_schema_json,
                                                section_list=section_list,
                                                error_code=error_code,
                                                row_num = row_index)

            # need to update the data report and list not append
            data_report_list.extend(row_report)        
            data_summary_list.extend(row_summary)

            # increase the row index
            row_index +=1

    return data_report_list,data_summary_list


def row_parser(row_data: str,data_schema_json: list,
                section_list: list,error_code: list,
                row_num: int) -> tuple:
    """
    Function to generate report for each data point

    Args:
        row_data: row data from the text file
        data_schema_json: json file containing standard definition of data
        section_list: list consists of all the sections from standard definition
        error_code: list consists of error code templates
        row_num: row number

    Returns:
        tuple: report, summary of each row

    """
    
    # report for each row
    row_report_list = []

    # summary for each row
    row_summary_list = []

    logger.info(f'Original row data from input file: {row_data}')
    # remove the new line character and separate the row based on delimiter '&'
    data_list = row_data.rstrip().split('&')
    logger.info(f'Sub_section values from (row {row_num}): {data_list[1:]}')

    
    # check the section value first
    if data_list[0] in section_list:
        col_summary_list = []

        section_value = data_list[0]
            
        # get the sub-section list    
        sub_section_list = hp.get_sub_section(standard_definition=data_schema_json,
                                                    section_name=data_list[0])
                
        logger.info(f'Sub-section list for {section_value} from data schema = {sub_section_list}')
            
        # track the column index
        col_index = 1 
        # loop through sub section in standard definition
        for expected_sub_section_key in sub_section_list:
            col_report_list = []
            # add section value
            col_report_list.append(section_value)
            logger.info(f'Upated column report with section: {section_value} = {col_report_list}')

            # add subsection value
            col_report_list.append(expected_sub_section_key)
            logger.info(f'Upated column report with subsection: {expected_sub_section_key} = {col_report_list}')

            logger.info(f'Column index: {col_index} == {expected_sub_section_key} ')
                
            if col_index < len(data_list):
                given_sub_section = data_list[col_index]
                col_report, data_type_flag, max_length_flag = data_validator(data_schema= data_schema_json,
                                                                            section_name = section_value,
                                                                            exp_sub_sec_key = expected_sub_section_key,
                                                                            given_sub_sec_val = given_sub_section)

                logger.info(f'Column report: {col_report}')
                # increase column index
                col_index +=1

                # extend the col_report_list with col_report
                col_report_list.extend(col_report)

                # call get_error_info function
                summary_msg, e_code = get_error_info(data_schema=data_schema_json,
                                                            section_value = section_value,
                                                            sub_section =  expected_sub_section_key,
                                                            error_code=error_code,
                                                            flag_data_type=data_type_flag,
                                                            flag_max_length=max_length_flag)

                # extend the error code
                col_report_list.extend([e_code])

                # append the summary message
                row_summary_list.append(summary_msg)

                logger.info(f'Extended column report list = {col_report_list}')
                logger.info(f'Summary message: {summary_msg} ')
                
            # missing value
            else:
                col_report, _, _ =  data_validator(data_schema= data_schema_json,
                                                    section_name = section_value,
                                                    exp_sub_sec_key = expected_sub_section_key,
                                                    given_sub_sec_val = None)

                # extend the col_report_list with col_report
                col_report_list.extend(col_report)

                logger.info('missing values')

                # summary message compilation
                e_code = error_code[4]['code']
                msg_format = error_code[4]['message_template']
                summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                            segment_name=section_value,
                                                            subsection = expected_sub_section_key)
                logger.info(f'Summary message: {summary_msg}')

                # again extend the list with error code
                col_report_list.extend([e_code])
                
                logger.info(f'Extended column report list = {col_report_list}')

                # add summary report 
                row_summary_list.append(summary_msg)
                # increase column index
                col_index +=1


            # append to row_report_list
            row_report_list.append(col_report_list)

        
    # should return summary and report list for each data line
    return row_report_list,row_summary_list


def data_validator(data_schema:list, section_name:str, exp_sub_sec_key:str, 
                        given_sub_sec_val: str) -> tuple:
    """
    Function to validate the data based on the data schema

    Args:

        report_list: list containing the report of sub_section

    Returns:
        tuple: report_list, flag_data_type, flag_max_length

    """
    # set flag for data_type and max_length to keep track of validation pass(True) or fail(False)
    flag_data_type = True
    flag_max_length = True

    # empty list for subsection report
    sub_section_report = []

    # get the data type and max length for sub key standard json
    exp_data_type, exp_max_length = hp.get_validation_criteria(data_schema_json = data_schema,
                                                                section=section_name,
                                                                sub_section=exp_sub_sec_key)

    logger.info(f'Expected data type = {exp_data_type} & max_length= {exp_max_length} from data schema')

    # empty data type and empty given length
    given_data_type = ''
    given_length = ''

    logger.info(f'Given value: {given_sub_sec_val}')
    # check for missing values
    if given_sub_sec_val != None:
        # if there is missing values
        if exp_data_type != None:
            
            if len(given_sub_sec_val.strip()) >0:
                
                # overwrite the given_length with length of input value
                given_length = len(given_sub_sec_val)

                # check for data type validation
                if given_sub_sec_val.replace(' ','').isalpha() and exp_data_type == 'word_characters':
                    
                    # set given data type
                    given_data_type = 'word_characters'

                elif given_sub_sec_val.isdigit() and exp_data_type == 'digits':

                    # set given data type
                    given_data_type = 'digits'
                # else if both data type validation fails
                else:

                    flag_data_type = False
                    # check data type of the value
                    if given_sub_sec_val.replace(' ','').isalpha():
                        given_data_type = 'word_characters'

                    elif given_sub_sec_val.isdigit():
                        given_data_type = 'digits'

                    else:
                        # set given data type
                        given_data_type = 'others'

                logger.info(f'Given data type = {given_data_type} and expected data type = {exp_data_type}')

                # check for length validation
                if given_length > exp_max_length:
                    flag_max_length = False

                logger.info(f'Given data length = {given_length} and expected max length = {exp_max_length}')

                logger.info(f'Data type validation ={flag_data_type} and max length validation = {flag_max_length}')
                                  
            # empty string
            else:
                flag_data_type = False
                flag_max_length = False


            # add given data type
            sub_section_report.append(given_data_type)
            sub_section_report.append(exp_data_type)
            sub_section_report.append(given_length)
            sub_section_report.append(exp_max_length)

            return sub_section_report, flag_data_type, flag_max_length

        else:
            logger.info(f'Discarded: sub section {exp_sub_sec_key} of {section_name} not in standard schema')

    # missing values
    else:
        logger.info('Missing values!!!')
        # return only the column report
        logger.info(f'Given value: {given_sub_sec_val}')
        # add given data type
        sub_section_report.append(given_data_type)
        sub_section_report.append(exp_data_type)
        sub_section_report.append(given_length)
        sub_section_report.append(exp_max_length)

        logger.info(f'Sub_section report from data_validator = {sub_section_report}')

        return sub_section_report, None, None
            


    # incase of the value is discarded 
    return None, None,None
    

def get_error_info(data_schema:list,section_value:str,sub_section:str, 
                    error_code:list,flag_data_type:bool, flag_max_length: bool) -> tuple:
    """
    Function to return error message based on flag value
    Args:
        error_code: list of error code
        flag_data_type: bool to indicate data type validation
        flag_max_length: bool to indicate max_length validation

    Returns:
        tuple: summary message, error code
    """

    # empty summary message
    summary_msg = ''
    # get the data type and max length for sub key standard json
    data_type, max_length = hp.get_validation_criteria(data_schema_json = data_schema,
                                                        section=section_value,
                                                        sub_section=sub_section)


    # condition for error message: error code = E01 code
    if flag_data_type == True and flag_max_length == True:
        logger.info('All condition are matched!!!')

        try:
            # summary message compilation
            e_code = error_code[0]['code']
            msg_format = error_code[0]['message_template']
            summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                    segment_name=section_value,
                                                    subsection = sub_section)

            logger.info(f'Summary message: {summary_msg}')
        except:
            logger.exception(f'error in summary message compilation')

    # E02
    elif flag_data_type == False and flag_max_length == True:
                                            
        logger.info('Only max length validation is passed')

        try:
            # summary message compilation
            e_code = error_code[1]['code']
            msg_format = error_code[1]['message_template']
            summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                    segment_name=section_value,
                                                    subsection = sub_section,
                                                    validation=(data_type, max_length))
                                                
            logger.info(f'Summary message: {summary_msg}')
        
        except:
            logger.exception(f'error in summary message compilation')

    # E03
    elif flag_data_type == True and flag_max_length == False:

        logger.info('Only data type validation is passed')

        try:
            # summary message compilation
            e_code = error_code[2]['code']
            msg_format = error_code[2]['message_template']
            summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                    segment_name=section_value,
                                                    subsection = sub_section,
                                                    validation=(data_type, max_length))
                                                
            logger.info(f'Summary message: {summary_msg}')
        except:
            logger.exception(f'error in summary message compilation')

                                    
    # else for error message: error code = E04
    else:
        logger.info('Nothing passed....')

        try:
            # summary message compilation
            e_code = error_code[3]['code']
            msg_format = error_code[3]['message_template']
            summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                    segment_name=section_value,
                                                    subsection = sub_section)
            logger.info(f'Summary message: {summary_msg}')
        except:
            logger.exception(f'error in summary message compilation')


    return summary_msg, e_code

    