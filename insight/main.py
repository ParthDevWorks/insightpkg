import logging
from datetime import datetime
from typing import Literal

from insight.config import load_config, PACKAGE_VERSION
from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries
from insight.db.insert import (
    insert_into_pypi_packages_table,
    insert_into_github_info_table,
    insert_into_github_release_notes_table,
)
from insight.decorator.main import timing_decorator
from insight.github.utils import (
    get_release_notes_info,
    get_repo_info,
)

logger = logging.getLogger(__name__)


@timing_decorator
def ingest_pypi(
    mode: Literal["dev", "prod"], dry_run: bool = False, minimum_stars: int = 10
) -> bool:
    try:
        pypi_ingest_status = False

        logger.info("=" * 60)
        logger.info(f"🚀 Run started at {datetime.now():%Y-%m-%d %H:%M:%S}")
        logger.info(f"Package Running in {mode!r} Mode")
        logger.info(f"Package Version:- {PACKAGE_VERSION!r}")
        if dry_run:
            logger.info(
                "Package Running in Dry Run Mode. No Database Entries will be made"
            )

        logger.info("=" * 60)

        config = load_config(section=mode)

        pypi_data = get_pypi_packages_uploaded_today()
        github_metadata = get_repo_info(pypi_data, minimum_stars=minimum_stars)
        release_notes_info = get_release_notes_info(github_metadata)

        if not dry_run:
            db = DatabaseEntries(config=config)
            conn = db.get_connection_object

            insert_into_pypi_packages_table(conn=conn, data=pypi_data)
            insert_into_github_info_table(conn=conn, data=github_metadata)
            insert_into_github_release_notes_table(conn=conn, data=release_notes_info)

            db.shutdown()

        pypi_ingest_status = True
    except Exception:
        logger.critical("PyPI Ingestion Pipeline Failed", exc_info=True)
        pypi_ingest_status = False

    return pypi_ingest_status
