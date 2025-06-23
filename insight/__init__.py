import os
import logging
from pathlib import Path
from importlib.metadata import version
from datetime import datetime

from insight.log.handler import MonthlyRotatingFileHandler

LOG_DIR = os.getenv("LOG_DIR", Path(__file__).parent.parent.resolve())
PACKAGE_VERSION = version("insight")


logger = logging.getLogger("insight")
logger.setLevel(logging.DEBUG)


monthly_handler = MonthlyRotatingFileHandler(Path(LOG_DIR))
formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
monthly_handler.setFormatter(formatter)
logger.addHandler(monthly_handler)

logger.info("=" * 60)
logger.info(f"🚀 Run started at {datetime.now():%Y-%m-%d %H:%M:%S}")
logger.info("=" * 60)
