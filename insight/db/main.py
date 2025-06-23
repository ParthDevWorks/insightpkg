import logging

from insight.db.utils import (
    load_config,
    create_database,
    create_required_tables,
    get_connection,
    insert_into_pypi_packages_table,
)

from insight.pypi.datatypes import RecentPackages

logger = logging.getLogger(__name__)


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
        self.ensure_database_is_ready()

        config = load_config()
        self.conn = get_connection(config)

        self.ensure_tables_are_present()

        self.data = data

    def ensure_database_is_ready(self):
        """
        Ensure the database is created.

        This method calls functions to create the database if it doesn't exist,
        """

        create_database()

    def ensure_tables_are_present(self):
        """
        Ensure the tables are set up.

        This method calls functions to create the required tables in the database.
        """
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
