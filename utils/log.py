import os
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING, StreamHandler
from logging import getLogger as _getLogger
from sys import stderr, stdout

from coloredlogs import ColoredFormatter

IS_DOCKER = os.path.exists('/.dockerenv')

def getLogger(name: str, level=DEBUG if not IS_DOCKER else INFO):
    logger = _getLogger(name)
    if logger.hasHandlers():
        return logger
    
    # YY-MM-DD HH:MM:SS [level:thread] name - message
    format = ColoredFormatter(
        fmt=f"%(asctime)s [%(levelname)s:%(threadName)s] %(name)s - %(message)s",
    )
    if IS_DOCKER:
        handler = StreamHandler(stderr)
    else:
        handler = StreamHandler(stdout)
    handler.setFormatter(format)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
