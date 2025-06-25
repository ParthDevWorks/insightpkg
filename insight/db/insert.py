import logging
from typing import Protocol, runtime_checkable

from psycopg2 import sql
from psycopg2.extensions import connection
from psycopg2.extras import execute_values

from insight.pypi.datatypes import RecentPackages
from insight.github.datatypes import GithubInfo

logger = logging.getLogger(__name__)


@runtime_checkable
class InsertableRecord(Protocol):
    def as_tuple(self) -> tuple: ...


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
    table_name = "pypi_packages"

    query = sql.SQL(
        """
        INSERT INTO {table_name} (
            package_name,
            package_version,
            package_upload_date,
            package_upload_time,
            package_github_link,
            package_description
        ) VALUES %s
        ON CONFLICT (package_name, package_version) DO NOTHING
    """
    ).format(table_name=sql.Identifier(table_name))

    bulk_insert(conn, data, query, table_name)


def insert_into_github_info_table(conn: connection, data: list[GithubInfo]):
    """
    Insert github information into the `github_info` table.

    This function inserts multiple rows of github metadata information into the
    github_info table using execute_values for better performance.

    Args:
        conn (connection): The database connection object.
        data (list[GithubInfo]): A list of GithubInfo objects containing
            the github metadata information to be inserted.
    """

    table_name = "github_info"

    query = sql.SQL(
        """
        INSERT INTO {table_name} (github_link, stars, watchers, forks, open_issues, created_date, last_updated_date, license)
        VALUES %s
        ON CONFLICT (github_link) DO UPDATE SET
            stars = EXCLUDED.stars,
            watchers = EXCLUDED.watchers,
            forks = EXCLUDED.forks,
            open_issues = EXCLUDED.open_issues,
            created_date = EXCLUDED.created_date,
            last_updated_date = EXCLUDED.last_updated_date,
            license = EXCLUDED.license;
        """
    ).format(table_name=sql.Identifier(table_name))

    bulk_insert(conn, data, query, table_name)


def bulk_insert(
    conn: connection,
    data: list[InsertableRecord],
    query: str,
    table_name: str,
) -> None:
    if not data:
        logger.info(f"No data to insert into {table_name}")
        return

    values = [item.as_tuple() for item in data]

    with conn.cursor() as cur:
        execute_values(cur, query, values)
    conn.commit()
    logger.debug(f"Data inserted into {table_name!r} table.")
