import logging

from insight.log.handler import FileHandlerLogger
from insight.config import LOG_DIR, PACKAGE_NAME


logger = logging.getLogger(PACKAGE_NAME)
logger.setLevel(logging.DEBUG)


file_handler = FileHandlerLogger(LOG_DIR)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
