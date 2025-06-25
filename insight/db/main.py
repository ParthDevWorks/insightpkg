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
        config (Config): The Config object.

    Usage:
        db = DatabaseEntries(config=config)
        conn = db.get_connection_object()
        func_name_which_inserts_data(conn, data)  # Inserts the data into the database
        db.shutdown()     # Closes the database connection

    Note:
        This class should be instantiated only once per session, typically in the main script.
    """

    def __init__(self, config: Config):
        self.config = config

        if self.config.mode == "dev":
            self.conn = self._load_dev_database()
        elif self.config.mode == "prod":
            self.conn = self._load_prod_database()

        self._ensure_tables_are_present()

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

    @property
    def get_connection_object(self):
        return self.conn

    def _ensure_tables_are_present(self):
        """
        Ensure the tables are set up.

        This method calls functions to create the required tables in the database.
        """
        create_required_tables(self.conn)

    def shutdown(self):
        """
        Close the database connection.

        This method closes the active database connection when the operation is complete.
        """

        self.conn.close()
