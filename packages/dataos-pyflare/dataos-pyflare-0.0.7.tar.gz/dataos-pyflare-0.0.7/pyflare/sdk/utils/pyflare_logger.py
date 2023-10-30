import logging

from pyflare.sdk.config.constants import get_log4j_properties_path, LOG4J_PROPERTIES
from pyflare.sdk.utils.generic_utils import write_string_to_file

global_logger = None


def setup_pyflare_logger(log_level="INFO", name=__name__):
    logging.basicConfig(level=logging.getLevelName(log_level.upper()),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m-%d %H:%M',
                        )
    logger = logging.getLogger(name)
    # s_logger = logging.getLogger('py4j.java_gateway')
    # s_logger.setLevel(logging.ERROR)
    return logger


def get_pyflare_logger(log_level="INFO", name=__name__):
    global global_logger
    if not global_logger:
        global_logger = setup_pyflare_logger(log_level, name)
    return global_logger


def create_log4j_on_disk(root_logger_level):
    log4j_properties = LOG4J_PROPERTIES.format(root_logger_level=log4j_log_level(root_logger_level))
    log4j_file_path = get_log4j_properties_path()
    write_string_to_file(file_path=log4j_file_path, string_data=log4j_properties)


def log4j_log_level(python_log_level):
    python_to_log4j_mapping = {
        "DEBUG": "DEBUG",
        "INFO": "INFO",
        "WARNING": "WARN",
        "ERROR": "ERROR",
        "CRITICAL": "FATAL"
    }
    return python_to_log4j_mapping[python_log_level.upper()]