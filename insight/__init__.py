import logging

from insight.log.handler import MonthlyRotatingFileHandler
from insight.config import LOG_DIR, PACKAGE_NAME


logger = logging.getLogger(PACKAGE_NAME)
logger.setLevel(logging.DEBUG)


monthly_handler = MonthlyRotatingFileHandler(LOG_DIR)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
monthly_handler.setFormatter(formatter)
logger.addHandler(monthly_handler)
