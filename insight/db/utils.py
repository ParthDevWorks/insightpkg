import os
from configparser import ConfigParser
from pathlib import Path
import logging
from typing import Literal

from psycopg2 import connect, sql
from psycopg2.extensions import connection
from psycopg2.extras import execute_values

from insight.pypi.datatypes import RecentPackages

DATABASE_INI_FILE_PATH = os.getenv("DATABASE_INI_FILE_PATH")
DEFAULT_DATABASE = "insightpkg"
MAINTENANCE_DB_NAME = "postgres"
DB_DIR = Path(__file__).parent.resolve()

logger = logging.getLogger(__name__)


def load_config(section: Literal["dev", "prod"]) -> dict:
    """
    Load configuration from the database ini file.

    This function reads the configuration from the specified ini file and returns
    a dictionary containing the parsed configuration parameters.

    Attributes:
        section (Literal[dev, prod]): The Section which defines what database needs to be loaded.
    Returns:
        dict: A dictionary containing the loaded configuration parameters.

    Raises:
        ValueError: If the environment variable 'DATABASE_INI_FILE_PATH' is not set.
        ValueError: If the DATABASE_INI_SECTION section is not found in the ini file.
    """

    if not DATABASE_INI_FILE_PATH:
        raise ValueError("Environment Variable 'DATABASE_INI_FILE_PATH' is not set")

    parser = ConfigParser()
    parser.read(DATABASE_INI_FILE_PATH)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise ValueError(
            f"Section {section!r} not found in the {DATABASE_INI_FILE_PATH} file"
        )
    return config


def get_connection(config: dict) -> connection:
    """
    Establish a connection to the PostgreSQL database.

    This function creates and returns a connection object to the specified
    PostgreSQL database using the provided configuration.

    Args:
        config (dict): A dictionary containing the database connection parameters.

    Returns:
        connection: A psycopg2 connection object to the database.
    """

    conn = connect(
        dbname=config["database"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
    )
    logger.debug(f"Connection established to Database {config["database"]!r}")
    return conn


# Since PostgreSQL doesn’t support CREATE DATABASE IF NOT EXISTS, We create a default connection to database which is 'postgres'
def check_maintenance_database(config: dict) -> connection:
    config_maintenance_copy = config.copy()

    config_maintenance_copy["database"] = MAINTENANCE_DB_NAME

    conn = get_connection(config_maintenance_copy)
    return conn


def create_database(config: dict) -> connection:
    """
    This function checks if the main database exists, and if not, creates it.
    It uses the default 'postgres' database to check for existence and create
    the main database if needed.

    Attributes:
        config (dict): A dictionary containing the database connection parameters.

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


def insert_into_pypi_packages_table(
    conn: connection, data: list[RecentPackages]
) -> None:
    """
    Insert package information into the `pypi_packages` table.

    This function inserts multiple rows of package information into the
    pypi_packages table using execute_values for better performance.

    Args:
        conn (connection): The database connection object.
        data (list[RecentPackages]): A list of RecentPackages objects containing
            the package information to be inserted.

    """
    if not data:
        logger.info("No Data to Insert in table")
        return

    values = [
        (
            p.package_name,
            p.package_version,
            p.package_upload_date,
            p.package_upload_time,
            p.package_github_link,
            p.package_description,
        )
        for p in data
    ]

    query = """
        INSERT INTO pypi_packages (
            package_name,
            package_version,
            package_upload_date,
            package_upload_time,
            package_github_link,
            package_description
        ) VALUES %s
        ON CONFLICT (package_name, package_version) DO NOTHING
    """

    with conn.cursor() as cur:
        execute_values(cur, query, values)
    conn.commit()

    logger.debug("Data has been inserted into 'pypi_packages' table.")
