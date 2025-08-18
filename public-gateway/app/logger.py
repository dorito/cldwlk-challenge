import logging

LOGGER = logging.getLogger("public-gateway")


def init_logging():
    logging.basicConfig(level=logging.DEBUG)
