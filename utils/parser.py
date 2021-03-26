import logging

from config import config
from log import logger
from utils import helper as hp


logger = logger.logger(__name__,logging.DEBUG)

def file_parser(input_path:str, data_schema_json: list,
                        section_list: list,error_code: list) -> tuple:
    """
    Function to parse the text file

    Args:
        data_schema_json: json file containing standard definition of data
        section_list: list consists of all the sections from standard definition
        error_code: list consists of error code templates
    Returns:
        tuple: report file as list of list and summary file as list
    """

    # two list one for summary and one for report
    summary_list = []

    #list of list to create report
    main_report_list = []

    # read the file
    with open(input_path,'r') as txt_file:
        # track the row number
        row_index =1

        for line in txt_file:
            # remove the new line character and separate the row based on delimiter '&'
            data_list = line.rstrip().split('&')
            logger.info(f'Sub_section values from (row {row_index}): {data_list[1:]}')
            
            # check the section value first
            if data_list[0] in section_list:
                # set flag for data_type and max_length to keep track of validation pass(1) or fail(-1)
                flag_data_type = 1
                flag_max_length = 1
                
                # track column index
                col_index = 1
                # check for the sub_section
                for sub_section in data_list[1:]:
                    # empty list for each sub section
                    report_list = []
                    try:
                        # get the sub section combining the main section and 
                        section_value = data_list[0]
                        # add section
                        report_list.append(section_value)
                        # sub section
                        sub_key = section_value+str(col_index)
                        # get the data type and max length for sub key standard json
                        data_type, max_length = hp.get_validation_criteria(data_schema_json,
                                                                                data_list[0],
                                                                                sub_key)

                        logger.info(f'Data type = {data_type} & max_length= {max_length} from data schema')

                        if data_type != None:
                            # add sub_section
                            report_list.append(sub_key)
                            logger.info(f'From: {sub_key} of section: {section_value} with subsection value: {sub_section}')

                            # check for missing values with white space
                            if len(sub_section.strip()) > 0:
                                # input length
                                input_data_len = len(sub_section)

                                if data_type == 'word_characters':
                                    # strip the space between char and check alphabet
                                    if not sub_section.replace(' ','').isalpha():
                                        flag_data_type = -1

                                        if sub_section.isdigit():
                                            # check value is all digit (doesn't include floating points)
                                            given_data_type = 'digits'
                                                
                                        else:
                                            # put the given data type as others
                                            given_data_type = 'others'
                                    else:
                                        # given data type is equivalent with expected data type
                                        given_data_type = data_type
                                            
                                    # check condtin for expected max_length
                                    if input_data_len > max_length:
                                        flag_max_length = -1

                                    # add given data type and expected data type to list
                                    report_list.append(given_data_type)
                                    report_list.append(data_type)

                                    # add given length and max length expected
                                    report_list.append(input_data_len)
                                    report_list.append(max_length)


                                elif data_type == 'digits':
                                    if not sub_section.isdigit():
                                        flag_data_type = -1

                                        if sub_section.replace(' ','').isalpha():
                                            given_data_type = 'word_characters'

                                        else:
                                            given_data_type = 'others'

                                    else:
                                        given_data_type = data_type
                                    
                                    # check condtin for expected max_length
                                    if input_data_len > max_length:
                                        flag_max_length = -1


                                    # add given data type and expected data type to list
                                    report_list.append(given_data_type)
                                    report_list.append(data_type)

                                    # add given length and max length expected
                                    report_list.append(input_data_len)
                                    report_list.append(max_length)



                                # condition for error message: error code = E01 code
                                if flag_data_type == 1 and flag_max_length == 1:
                                    logger.info('All condition are matched!!!')

                                    # summary message compilation
                                    e_code = error_code[0]['code']
                                    msg_format = error_code[0]['message_template']
                                    summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                                        segment_name=section_value,
                                                                        field_num = col_index)

                                    logger.info(f'Summary message: {summary_msg}')
                                    summary_list.append(summary_msg)

                                    # append the error code
                                    report_list.append(e_code)

                                # E02
                                elif flag_data_type == -1 and flag_max_length == 1:
                                        
                                    logger.info('Only max length validation is passed')
                                    # set back flag data type to 1
                                    flag_data_type = 1
                                    logger.info(f'Setting back the flag data type to {flag_data_type}')  

                                    # summary message compilation
                                    e_code = error_code[1]['code']
                                    msg_format = error_code[1]['message_template']
                                    summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                                        segment_name=section_value,
                                                                        field_num = col_index,
                                                                        validation=(data_type, max_length))
                                        
                                    logger.info(f'Summary message: {summary_msg}')
                                    summary_list.append(summary_msg)

                                    # append the error code
                                    report_list.append(e_code)

                                # E03
                                elif flag_data_type == 1 and flag_max_length == -1:

                                    logger.info('Only data type validation is passed')
                                    # set back max length flag to 1
                                    flag_max_length = 1
                                    logger.info(f'Setting back the flag max length to {flag_max_length}')

                                    # summary message compilation
                                    e_code = error_code[2]['code']
                                    msg_format = error_code[2]['message_template']
                                    summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                                        segment_name=section_value,
                                                                        field_num = col_index,
                                                                        validation=(data_type, max_length))
                                        
                                    logger.info(f'Summary message: {summary_msg}')
                                    summary_list.append(summary_msg)

                                    # append the error code
                                    report_list.append(e_code)
                                    
                                # else for error message: error code = E04
                                else:
                                    logger.info('Nothing passed....')

                                    # set back both the flags to 1 
                                    flag_max_length = 1
                                    logger.info(f'Setting back the flag max length to {flag_max_length}')
                                    flag_data_type = 1
                                    logger.info(f'Setting back the flag data type to {flag_data_type}')

                                    # summary message compilation
                                    e_code = error_code[3]['code']
                                    msg_format = error_code[3]['message_template']
                                    summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                                        segment_name=section_value,
                                                                        field_num = col_index)
                                    logger.info(f'Summary message: {summary_msg}')
                                    summary_list.append(summary_msg)

                                    # append the error code
                                    report_list.append(e_code)
                                
                            # else condition for missing values: error code = E05
                            else:
                                logger.info('missing values')

                                # summary message compilation
                                e_code = error_code[4]['code']
                                msg_format = error_code[4]['message_template']
                                summary_msg  = hp.summary_msg_formatter(msg_format=msg_format,
                                                                            segment_name=section_value,
                                                                            field_num = col_index)
                                logger.info(f'Summary message: {summary_msg}')
                                summary_list.append(summary_msg)

                                # add given data type and expected data type to list
                                report_list.append('')
                                report_list.append(data_type)

                                # add given length and max length expected
                                report_list.append('')
                                # no data in standard definition
                                report_list.append(None)

                                # append the error code
                                report_list.append(e_code)


                            # report for each sub section 
                            logger.info(f'Report from {section_value}:{sub_key} for (row: {row_index}): {report_list}')
                            

                            # add the row report to main report list
                            main_report_list.append(report_list)

                            # increase col_index
                            col_index +=1

                        # else condition if the sub section of segment is not in standard definition
                        else:
                            summary_list.append(f'Discarded: sub section {sub_key} of {section_value} not in standard schema')
                        

                    except:
                        # set the logger here.
                        logger.exception('Error!!! ')

                # increase the row index
                row_index += 1
            
           


    return main_report_list,summary_list