from config import config
from utils import parser


def test_file_parser(standard_definition,
                    section_list,error_definition):
    """ Tests file parser """

    report,summary = parser.file_parser(input_path=config.TEST_DATA_PATH,
                                    data_schema_json=standard_definition,
                                    section_list=section_list,
                                    error_code=error_definition)

    
    assert isinstance(report,list)== True
    assert isinstance(summary,list)== True

