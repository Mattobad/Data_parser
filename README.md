# Overview
BlueNode interview assignment

## Technologies used:
**Python Version:** 3.8
**Other packages:** pandas, pytest, pymake

## Environment setup

**Anaconda:** 
```
$ conda create --name ENVNAME python=3.8
$ conda activate ENVNAME
$ pip install -r requirements.txt
```
**VirtualEnv:**
```
$ pip install virtualenv
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```


## How to run locally:

Command to execute the code:
`$ pymake local_dev`

Command to execute the test suite:
`$ pymake test`

### Directory Structure
  ``` .
      ├──.github/workflow
      │   └── python-app.yml
      ├── config 
      │   └── config.py    
      ├── data
      │   ├── parsed   
      │   │   ├── report.csv
      │   │   └── summary.txt
      │   ├── sample
      │   │   ├── report.csv
      │   │   └── summary.txt
      │   ├── tests
      │   │   ├── test_file.txt
      │   │   ├── test_report.csv
      │   │   └── test_summary.txt
      │   ├── error_codes.json
      │   ├── input_file.txt
      │   └── standard_definition.json
      ├── log
      │   └── logger.py
      ├── tests
      │   ├── conftest.py         
      │   ├── test_config.py
      │   ├── test_helper.py
      │   └── test_parser.py
      ├── utils
      │   ├── helper.py
      │   └── parser.py
      ├── INSTRUCTIONS.md
      ├── Makefile   
      ├── README.md  
      ├── main.py
      └── requirements.txt
      
      
      



      
