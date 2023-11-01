import logging


def get_logger(name: str = "roseta", level: str = "info") -> logging.Logger:
    logger = logging.getLogger(name)

    level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    logger.setLevel(level_dict[level])

    if not logger.handlers:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console_fmt = logging.Formatter("%(filename)s %(levelname)s %(lineno)d: %(message)s")
        console.setFormatter(console_fmt)
        logger.addHandler(console)
    return logger
