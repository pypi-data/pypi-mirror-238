import logging
import os

ROOT = os.getcwd()

SUCCESS = 21
FAIL = 16
PIPE = 17
LOG_LEVEL = logging.INFO
LOG_LEVEL_E = logging.WARNING
LOGFORMAT = '%(log_color)s%(asctime) s%(reset)s |%(log_color)s %(filename)s:%(name)s%(reset)s |%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s | level=%(levelname)s%(reset)s'
LOGFORMAT_ERROR = '%(log_color)s%(asctime)s %(reset)s | %(log_color)s %(filename)s:%(name)s%(reset)s | %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s | level=%(levelname)s%(reset)s'

LOG_COLORS = {
    'DEBUG': 'white,bg_black',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_black',
    'SUCCESS': 'bold_green',
    'FAIL': 'white,bg_black',
    'PIPE': 'green',
}
