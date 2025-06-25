import logging
from datetime import datetime
from typing import Literal

from insight.config import load_config, PACKAGE_VERSION
from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries
from insight.db.insert import (
    insert_into_pypi_packages_table,
    insert_into_github_info_table,
)
from insight.db.select import github_repos_metadata
from insight.decorator.main import timing_decorator

logger = logging.getLogger(__name__)


@timing_decorator
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

        db = DatabaseEntries(config=config)
        conn = db.get_connection_object

        insert_into_pypi_packages_table(conn=conn, data=data)

        db.shutdown()

        pypi_ingest_status = True
    except Exception:
        logger.critical("Ingest Pipeline Failed", exc_info=True)
        pypi_ingest_status = False

    return pypi_ingest_status


@timing_decorator
def post_to_reddit(mode: Literal["dev", "prod"]) -> bool:
    try:
        post_reddit_status = False

        logger.info("=" * 60)
        logger.info(f"🚀 Run started at {datetime.now():%Y-%m-%d %H:%M:%S}")
        logger.info(f"Package Running in {mode!r} Mode")
        logger.info(f"Package Version:- {PACKAGE_VERSION!r}")
        logger.info("=" * 60)

        config = load_config(section=mode)

        db = DatabaseEntries(config=config)
        conn = db.get_connection_object

        data = github_repos_metadata(conn=conn)

        insert_into_github_info_table(conn=conn, data=data)

        db.shutdown()

        post_reddit_status = True
    except Exception:
        logger.critical("Reddit Post Failed", exc_info=True)
        post_reddit_status = False

    return post_reddit_status
