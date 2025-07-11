"""dash_config.py
Used to configure aspects of dash gui
"""
from os import environ
#MOCK_EPMT_API = environ.get('EPMT_GUI_MOCK')
MOCK_EPMT_API = False

DEBUG = environ.get('DASH_DEBUG')

DEFAULT_ROWS_PER_PAGE = 30

# Job columns in order
columns_to_print = ['jobid', 'exit_code', 'Processed', 'start', 'end', 'duration', 'usertime', 'systemtime',
                    'cpu_time', 'write_bytes', 'read_bytes', 'tags']

# Job tags in order to display as columns
tags_to_display = ['exp_name', 'exp_component', 'atm_res', 'ocn_res']

# todo: reorganize columns
# https://stackoverflow.com/a/25122293/10434952
