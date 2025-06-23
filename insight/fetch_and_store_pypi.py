from insight.pypi.utils import get_pypi_packages_uploaded_today
from insight.db.main import DatabaseEntries


def execute():

    data = get_pypi_packages_uploaded_today()

    db = DatabaseEntries(data=data)
    db.insert_data()
    db.shutdown()
