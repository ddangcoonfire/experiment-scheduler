"""
setting for logger
"""
import logging

FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)
RESET_END = "\u001b[0m"
LEVEL_COLOR_MAP = {
    logging.DEBUG: "\u001b[36m [DEBUG] " + FORMAT + RESET_END,
    logging.INFO: "\u001b[32m [INFO] " + FORMAT + RESET_END,
    logging.WARNING: "\u001b[33m [WARN] " + FORMAT + RESET_END,
    logging.ERROR: "\u001b[31m [ERROR] " + FORMAT + RESET_END,
}


def get_logger(name, *args, **kwargs):
    """
    set logger with certain configuration
    :param name: logger's name
    :param args: add logger setting
    :param kwargs: add logger setting
    :return:
    """
    logger = logging.getLogger(name=name, *args, **kwargs)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomLoggingFormatter())
    file_handler = logging.FileHandler(f"{name}.log")
    file_handler.setFormatter(CustomLoggingFormatter())
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


def start_end_logger(func):
    """
    decorator for logging function's start and end point
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        self.logger.info(f"{func.__name__} starts")
        result = func(self, *args, **kwargs)
        self.logger.info(f"{func.__name__} finished")
        return result

    return wrapper


class CustomLoggingFormatter(logging.Formatter):
    """
    custom logging
    """

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = LEVEL_COLOR_MAP.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
