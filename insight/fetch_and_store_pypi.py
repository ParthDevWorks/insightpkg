import logging
from datetime import datetime
from typing import Literal

from insight import PACKAGE_VERSION
from insight.config import load_config
from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries

logger = logging.getLogger(__name__)


def execute(mode: Literal["dev", "prod"]):
    logger.info("=" * 60)
    logger.info(f"🚀 Run started at {datetime.now():%Y-%m-%d %H:%M:%S}")
    logger.info(f"Package Running in {mode!r} Mode")
    logger.info("=" * 60)
    logger.info(f"Package Version:- {PACKAGE_VERSION!r}")

    config = load_config(section=mode)
    data = get_pypi_packages_uploaded_today()

    db = DatabaseEntries(config=config, data=data)
    db.insert_data()
    db.shutdown()
