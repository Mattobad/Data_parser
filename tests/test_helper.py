from utils import helper as hp
from config import config

"""
Unit test for helper module
"""



# test the output of get_sections_list function
def test_get_section(standard_definition,section_list):
    """ Tests the section values in standard definition file """

    # when
    sections = hp.get_sections_list(json_file=standard_definition)

    #then
    assert len(sections) == len(section_list)

    assert isinstance(sections,list) == True
    assert len(set(sections) - set(section_list)) == 0


def test_validation_criteria(standard_definition,section_dict):
    """ Tests the validation criteria types for each sections """

    # when 
    for section,sub_section_arr in section_dict.items():
        
        for sub_section in sub_section_arr:
            data_type,max_length = hp.get_validation_criteria(
                                            data_schema_json=standard_definition,
                                            section=section,
                                            sub_section=sub_section)

            if sub_section != 'L33':
                assert data_type in ['digits','word_characters']
                assert isinstance(data_type,str) == True
                assert isinstance(max_length,int) == True
            else:
                assert data_type == None
                assert max_length == 'value not found!!'


def test_error_code(error_definition):
    """ Tests given error code keys """

    for error_code in error_definition:
        # check for dictionary content
        for key,value in error_code.items():
            assert key in ['code','message_template']
            assert isinstance(key,str)==isinstance(value,str) == True

def test_msg_formatter(standard_definition,error_definition,
                                                section_list,
                                                section_dict):
    """ Tests the type of message formatter """
    
    error_template = error_definition[0]['message_template']

    segment = section_list[0]
    sub_section = section_dict[segment][0]
    summary_msg = hp.summary_msg_formatter(msg_format=error_template,
                                            segment_name=segment,
                                            subsection=sub_section)

    data_type,max_length = hp.get_validation_criteria(
                                            data_schema_json=standard_definition,
                                            section=segment,
                                            sub_section=sub_section)

    summary_msg1 = hp.summary_msg_formatter(msg_format=error_template,
                                            segment_name=segment,
                                            subsection=sub_section,
                                            validation=(data_type, 
                                                        max_length)
                                            )

    assert isinstance(summary_msg,str) == True
    assert isinstance(summary_msg1,str) == True


def test_save_csv(summary_report):
    """ Tests save to csv function """

    report, _ = summary_report

    result = hp.save_to_csv(report=report,
                            report_path=config.TEST_REPORT_PATH)

    assert isinstance(result,bool) == True
 

def test_save_txt(summary_report):
    """ Tests save to csv function """

    _, summary = summary_report

    result = hp.save_to_txt(summary=summary,
                                dest_path=config.TEST_SUMMARY_PATH)

    assert isinstance(result,bool) == True

                                            