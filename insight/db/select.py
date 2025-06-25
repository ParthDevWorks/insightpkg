import logging

from psycopg2 import sql
from psycopg2.extensions import connection

from insight.github.utils import get_repo_info
from insight.github.datatypes import GithubInfo

logger = logging.getLogger(__name__)


def github_repos_metadata(conn: connection) -> list[GithubInfo]:
    """
    Retrieves GitHub Repo Metadata Info for PyPI packages stored in the database.

    Args:
        conn (psycopg2.extensions.connection): A PostgreSQL database connection object.

    Returns:
        list[GithubInfo]: A list of GithubInfo objects containing GitHub repository information.

    Note:
        Ensure that the 'pypi_packages' table contains the required 'package_github_link' column before executing this function.
    """

    output = []
    table_name = "pypi_packages"
    column_name_required = "package_github_link"

    query = sql.SQL("Select DISTINCT {column} FROM {table}").format(
        column=sql.Identifier(column_name_required), table=sql.Identifier(table_name)
    )

    with conn.cursor() as cur:
        cur.execute(query)
        all_repo_urls = cur.fetchall()

    for url in all_repo_urls:
        required_url = url[0]
        if required_url:
            try:
                repo_info = get_repo_info(repo_url=required_url)
                output.append(repo_info)
            except Exception:
                pass

    return output
