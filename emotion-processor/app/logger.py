import logging

LOGGER = logging.getLogger('emotion-processor')

def init_logging():
  logging.basicConfig(level=logging.DEBUG)
  logger = logging.getLogger('kafka') # mute some annoying logs
  logger.setLevel(logging.FATAL)