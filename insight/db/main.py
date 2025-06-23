from insight.db.utils import (
    load_config,
    create_database,
    create_required_tables,
    get_connection,
    insert_into_pypi_packages_table,
)

from insight.pypi.datatypes import RecentPackages


class DatabaseEntries:
    """
    Manages database operations for storing and retrieving package information.

    This class encapsulates the logic for connecting to the database, ensuring
    it's ready for use, inserting data, and shutting down connections when done.

    Attributes:
        conn (connection): The database connection object.
        data (list[RecentPackages]): The list of RecentPackages objects to be inserted.

    Usage:
        db = DatabaseEntries(data=recent_packages_list)
        db.insert_data()  # Inserts the data into the database
        db.shutdown()     # Closes the database connection

    Note:
        This class should be instantiated only once per session, typically in the main script.
    """

    def __init__(self, data: list[RecentPackages]):
        config = load_config()
        self.conn = get_connection(config)
        self.ensure_database_is_ready()
        self.data = data

    def ensure_database_is_ready(self):
        """
        Ensure the database is created and tables are set up.

        This method calls functions to create the database if it doesn't exist,
        and creates the required tables in the database.
        """

        create_database()
        create_required_tables(self.conn)

    def insert_data(self):
        """Insert the stored data into the database."""

        insert_into_pypi_packages_table(self.conn, self.data)

    def shutdown(self):
        """
        Close the database connection.

        This method closes the active database connection when the operation is complete.
        """

        self.conn.close()


# For Testing Purpose
if __name__ == "__main__":
    from insight.pypi.utils import get_pypi_packages_uploaded_today

    data = get_pypi_packages_uploaded_today()

    db = DatabaseEntries(data=data)
    db.insert_data()
    db.shutdown()
