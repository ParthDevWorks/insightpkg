import logging
from datetime import datetime
from typing import Literal

from insight.config import load_config, PACKAGE_VERSION
from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries

logger = logging.getLogger(__name__)


def ingest_pypi(mode: Literal["dev", "prod"]) -> bool:
    try:
        pypi_ingest_status = False

        logger.info("=" * 60)
        logger.info(f"🚀 Run started at {datetime.now():%Y-%m-%d %H:%M:%S}")
        logger.info(f"Package Running in {mode!r} Mode")
        logger.info(f"Package Version:- {PACKAGE_VERSION!r}")
        logger.info("=" * 60)

        config = load_config(section=mode)
        data = get_pypi_packages_uploaded_today()

        db = DatabaseEntries(config=config, data=data)
        db.insert_data()
        db.shutdown()

        pypi_ingest_status = True
    except Exception:
        logger.critical("Ingest Pipeline Failed", exc_info=True)
        pypi_ingest_status = False

    return pypi_ingest_status
