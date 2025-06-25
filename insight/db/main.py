import logging
import psycopg2
from psycopg2.extensions import connection

from insight.db.utils import (
    create_database,
    create_required_tables,
    insert_into_pypi_packages_table,
)

from insight.config import Config
from insight.pypi.datatypes import RecentPackages

logger = logging.getLogger(__name__)


class DatabaseEntries:
    """
    Manages database operations for storing and retrieving package information.

    This class encapsulates the logic for connecting to the database, ensuring
    it's ready for use, inserting data, and shutting down connections when done.

    Attributes:
        mode (Literal["dev", "prod"]): The database mode.
        data (list[RecentPackages]): The list of RecentPackages objects to be inserted.

    Usage:
        db = DatabaseEntries(mode="dev", data=recent_packages_list)
        db.insert_data()  # Inserts the data into the database
        db.shutdown()     # Closes the database connection

    Note:
        This class should be instantiated only once per session, typically in the main script.
    """

    def __init__(self, config: Config, data: list[RecentPackages]):
        self.config = config

        if self.config.mode == "dev":
            self.conn = self._load_dev_database()
        elif self.config.mode == "prod":
            self.conn = self._load_prod_database()

        self._ensure_tables_are_present()

        self.data = data

    def _load_dev_database(self) -> connection:
        """
        Ensure the Development System Database is ready.

        Returns:
            conn: A psycopg2 connection object to the dev database.
        """

        conn = create_database(config=self.config)
        return conn

    def _load_prod_database(self) -> connection:
        """
        Ensure the Production System Database is ready.

        Returns:
            conn: A psycopg2 connection object to the prod database.
        """
        connection_string = f"postgresql://{self.config.db_user}:{self.config.db_password}@{self.config.db_host}:{self.config.db_port}/{self.config.db_database_name}"
        conn = psycopg2.connect(connection_string)
        return conn

    def _ensure_tables_are_present(self):
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
