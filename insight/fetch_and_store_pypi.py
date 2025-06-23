import logging

from insight import PACKAGE_VERSION
from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries

logger = logging.getLogger(__name__)


def execute():
    logger.info(f"Package Version:- {PACKAGE_VERSION!r}")

    data = get_pypi_packages_uploaded_today()

    db = DatabaseEntries(data=data)
    db.insert_data()
    db.shutdown()
