import logging
from logging.handlers import RotatingFileHandler

LOGGER_NAME = "bookmark-api"


def setup_logging() -> None:
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = RotatingFileHandler("app.log", maxBytes=100_000, backupCount=3)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)
