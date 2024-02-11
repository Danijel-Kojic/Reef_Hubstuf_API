import os
from dotenv import load_dotenv
import platform
import logging

LOG_FILE_PATH = 'D:\\reef.log' if platform.system() == 'Windows' else '/tmp/reef.log'

root_loggers = {}

def get_root_logger(logger_name, filename=None):
    load_dotenv()
    global root_loggers
    if logger_name in root_loggers:
        return root_loggers[logger_name]
    ''' get the logger object '''
    logger = logging.getLogger(logger_name)
    # debug = os.getenv('ENV', 'development') == 'development'
    # logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if None == filename:
        filename = LOG_FILE_PATH

    # if debug:
    #     ch = logging.StreamHandler()
    #     ch.setFormatter(formatter)
    #     logger.addHandler(ch)

    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    root_loggers[logger_name] = logger
    return logger


def get_child_logger(root_logger, name):
    return logging.getLogger('.'.join([root_logger, name]))