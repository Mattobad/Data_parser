from config import config


def test_input_file_names(input_files):
    """ Tests input files names """

    stand_definition, input_file, error_file = input_files

    assert stand_definition == config.DATA_SCHEMA_FILE
    assert input_file == config.INPUT_FILE
    assert error_file == config.ERROR_CODE_FILE



def test_output_files_name(output_files):
    """ Tests output files names """

    report_file, summary_file = output_files

    assert report_file == config.REPORT_FILE
    assert summary_file == config.SUMMARY_FILE


def test_input_files_path(input_file_paths):
    """ Tests input files path """

    stand_def_path,input_path,error_code_path = input_file_paths

    assert stand_def_path == config.DATA_SCHEMA_PATH
    assert input_path == config.INPUT_PATH
    assert error_code_path == config.ERROR_CODE_PATH



def test_output_files_path(output_file_paths):
    """ Tests output files path """

    report_path,summary_path = output_file_paths

    assert report_path == config.REPORT_PATH
    assert summary_path == config.SUMMARY_PATH


def test_report_columns(report_cols):
    """ Tests report columns """

    assert isinstance(config.REPORT_COLMNS,list) == True
    assert len(set(report_cols) - set(config.REPORT_COLMNS)) == 0