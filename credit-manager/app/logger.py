import logging

from app.config import Config

LOGGER = logging.getLogger(Config.APP_NAME)


def init_logging():
    logging.basicConfig(level=logging.DEBUG)
    # mute some annoying logs
    logger = logging.getLogger("kafka")
    logger.setLevel(logging.FATAL)
    logger = logging.getLogger("celery")
    logger.setLevel(logging.INFO)
