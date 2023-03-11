import logging

_format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
)
_reset_end = "\u001b[0m"
_level_color_map = {
    logging.DEBUG: "\u001b[36m [DEBUG] " + _format + _reset_end,
    logging.INFO: "\u001b[32m [INFO] " + _format + _reset_end,
    logging.WARNING: "\u001b[33m [WARN] " + _format + _reset_end,
    logging.ERROR: "\u001b[31m [ERROR] " + _format + _reset_end,
}


def get_logger(name, *args, **kwargs):
    logger = logging.getLogger(name=name, *args, **kwargs)
    ch = logging.StreamHandler()
    ch.setFormatter(CustomLoggingFormatter())
    fh = logging.FileHandler(f"{name}.log", encoding="utf-8")
    fh.setFormatter(CustomLoggingFormatter())
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    return logger


def start_end_logger(func):
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
        log_fmt = _level_color_map.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
