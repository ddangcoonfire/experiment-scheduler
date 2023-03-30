"""
all logging method use get_logger.
"""
import logging

_LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)
_RESET_END = "\u001b[0m"
_LEVEL_COLOR_MAP = {
    logging.DEBUG: "\u001b[36m [DEBUG] " + _LOG_FORMAT + _RESET_END,
    logging.INFO: "\u001b[32m [INFO] " + _LOG_FORMAT + _RESET_END,
    logging.WARNING: "\u001b[33m [WARN] " + _LOG_FORMAT + _RESET_END,
    logging.ERROR: "\u001b[31m [ERROR] " + _LOG_FORMAT + _RESET_END,
}


def get_logger(name, *args, **kwargs):
    """
    returns logger for class.
    usage:
        class Master:
            self.logger = get_logger("master")
    with args and kwargs, Any configuration about logger can be tossed
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    logger = logging.getLogger(name=name, *args, **kwargs)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomLoggingFormatter())
    file_handler = logging.FileHandler(f"{name}.log", encoding="utf-8")
    file_handler.setFormatter(CustomLoggingFormatter())
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def start_end_logger(func):
    """
    Logging for request notification.
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
        log_fmt = _LEVEL_COLOR_MAP.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
