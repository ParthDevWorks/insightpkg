from pathlib import Path
import logging

from psycopg2 import connect, sql
from psycopg2.extensions import connection

from insight.config import Config

DEFAULT_DATABASE = "insightpkg"
MAINTENANCE_DB_NAME = "postgres"
DB_DIR = Path(__file__).parent.resolve()

logger = logging.getLogger(__name__)


def get_connection(config: Config) -> connection:
    """
    Establish a connection to the PostgreSQL database.

    This function creates and returns a connection object to the specified
    PostgreSQL database using the provided configuration.

    Args:
        config (Config): A config containing the database connection parameters.

    Returns:
        connection: A psycopg2 connection object to the database.
    """

    conn = connect(
        dbname=config.db_database_name,
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
    )
    logger.debug(f"Connection established to Database {config.db_database_name!r}")
    return conn


# Since PostgreSQL doesn’t support CREATE DATABASE IF NOT EXISTS, We create a default connection to database which is 'postgres'
def check_maintenance_database(config: Config) -> connection:
    config_maintenance_copy = config.model_copy()

    config_maintenance_copy.db_database_name = MAINTENANCE_DB_NAME

    conn = get_connection(config_maintenance_copy)
    return conn


def create_database(config: Config) -> connection:
    """
    This function checks if the main database exists, and if not, creates it.
    It uses the default 'postgres' database to check for existence and create
    the main database if needed.

    Attributes:
        config (Config): A config containing the database connection parameters.

    Returns:
        conn: A psycopg2 connection object to the database.

    """

    # Connect to the default 'postgres' database
    default_connection = check_maintenance_database(config=config)
    default_connection.autocommit = True
    default_cursor = default_connection.cursor()

    default_cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s", (DEFAULT_DATABASE,)
    )
    exists = default_cursor.fetchone()

    if not exists:
        default_cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DEFAULT_DATABASE))
        )
        logger.debug(f"Database {DEFAULT_DATABASE!r} created.")
    else:
        logger.debug(f"Database {DEFAULT_DATABASE!r} already exists.")

    conn = get_connection(config)
    return conn


def create_required_tables(conn: connection) -> None:
    """
    Create the required tables in the database.

    This function reads the SQL schema from a file and executes it to create
    the necessary tables in the database.

    Args:
        conn (connection): The database connection object.

    """

    schema_file_path = DB_DIR / "schema.sql"
    try:
        with open(schema_file_path, "r") as file:
            sql_script = file.read()

        cur = conn.cursor()
        cur.execute(sql_script)
        conn.commit()
        logger.debug("SQL Tables executed successfully.")

    except FileNotFoundError:
        logger.critical(f"Schema File not found at location: {schema_file_path!r}")
