import os
import logging
from pathlib import Path
from importlib.metadata import version

from insight.log.handler import MonthlyRotatingFileHandler

LOG_DIR = os.getenv("LOG_DIR", Path(__file__).parent.parent.resolve())
PACKAGE_NAME = "insight"
PACKAGE_VERSION = version(PACKAGE_NAME)


logger = logging.getLogger(PACKAGE_NAME)
logger.setLevel(logging.DEBUG)


monthly_handler = MonthlyRotatingFileHandler(Path(LOG_DIR))
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
monthly_handler.setFormatter(formatter)
logger.addHandler(monthly_handler)


def disable_logs():
    logger.disabled = True
    logger.propagate = False
    for name in list(logging.root.manager.loggerDict):
        if name.startswith(PACKAGE_NAME):
            logging.getLogger(name).disabled = True
            logging.getLogger(name).propagate = False
