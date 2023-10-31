"""Log initiation."""

import logging
import pathlib
from logging import handlers

from xdg_base_dirs import xdg_data_home

FILE_NAME: str = "metamock.log"
MAX_LOG_SIZE: int = 1000000  # 1MB
MAX_NO_OF_BACKUP_FILES: int = 10


def create_logger(name: str) -> logging.Logger:
    """Init a logger with name as parameter."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_directory = xdg_data_home()
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    log_file_path = log_directory / FILE_NAME

    rotating_handler = handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=MAX_NO_OF_BACKUP_FILES,
        mode="a",
    )

    rotating_handler.encoding = "utf-8"
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)

    return logger
