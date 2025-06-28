from datetime import datetime
import re
import logging

from insight.config import REQUEST_TOKEN
from insight.pypi.utils import get_request
from insight.pypi.datatypes import RecentPackages
from insight.github.datatypes import GithubInfo, GithubReleaseNotes

TIMEZONE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

logger = logging.getLogger(__name__)


def _get_owner_info(repo_url: str) -> tuple[str | None, str | None]:
    """
    Fetches and returns owner and repo_name information about a GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        owner (str | None): Owner of the Github Repository or None.
        repo (str | None): Repo of the Github Repository or None.

    """

    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)

    if match:
        owner, repo = match.group(1), match.group(2)
        if owner is None or repo is None:
            logger.warning(
                f"Owner :{owner} or Repo:{repo} is not correct for github url: {repo_url!r}"
            )
            return None, None

        return owner, repo
    else:
        return None, None


def get_repo_info(
    packages: list[RecentPackages], minimum_stars: int
) -> list[GithubInfo]:
    """
    Fetches and returns information about a GitHub repository.

    Args:
        packages (list[RecentPackages]): A list of RecentPackages dataclass.
        minimum_stars (int): Specifies the minimum number of GitHub stars required for a package to be stored in the database.

    Returns:
        list[GithubInfo]: List of objects containing detailed information about the repository.

    """
    github_info_metadata = []
    for item in packages:
        try:
            repo_url = item.package_github_link

            if not repo_url:
                continue

            owner, repo = _get_owner_info(repo_url=repo_url)

            if owner is None or repo is None:
                continue

            # GitHub API endpoint
            api_url = f"https://api.github.com/repos/{owner}/{repo}"

            response = get_request(api_url, auth=("username", REQUEST_TOKEN))

            data = response.json()

            created_date_iso = datetime.strptime(
                data.get("created_at"), TIMEZONE_FORMAT
            )
            created_date = created_date_iso.strftime("%Y-%m-%d")

            last_updated_iso = datetime.strptime(
                data.get("updated_at"), TIMEZONE_FORMAT
            )
            last_updated_date = last_updated_iso.strftime("%Y-%m-%d")

            stars = int(data.get("stargazers_count", 0))
            watchers = int(data.get("subscribers_count", 0))
            forks = int(data.get("forks_count", 0))
            open_issues = int(data.get("open_issues_count", 0))

            if stars < minimum_stars:
                logger.warning(
                    f"The github link {repo_url!r} has less than the minumum stars specified. Hence it wont be entered into Database"
                )
                continue

            github_info_metadata.append(
                GithubInfo(
                    github_link=repo_url,
                    stars=stars,
                    watchers=watchers,
                    forks=forks,
                    open_issues=open_issues,
                    created_date=created_date,
                    last_updated_date=last_updated_date,
                    license=(
                        data.get("license").get("name", None)
                        if data.get("license")
                        else None
                    ),
                )
            )
        except Exception:
            pass

    return github_info_metadata


def get_release_notes_info(
    github_metadata: list[GithubInfo],
) -> list[GithubReleaseNotes]:
    """
    Fetches and returns Release Notes Information about a GitHub repository.

    Args:
        github_metadata (list[GithubInfo]): A list of the GitHub repositorys metadata.

    Returns:
        list[GithubReleaseNotes]: A list of objects containing detailed release notes information about the repository.

    """
    release_info = []
    for item in github_metadata:
        try:
            repo_url = item.github_link

            if not repo_url:
                continue

            owner, repo = _get_owner_info(repo_url=repo_url)

            if owner is None or repo is None:
                continue

            # GitHub API endpoint
            api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

            response = get_request(api_url, auth=("username", REQUEST_TOKEN))

            data = response.json()
            latest_data = data[0]

            published_date_iso = datetime.strptime(
                latest_data.get("published_at"), TIMEZONE_FORMAT
            )
            published_date = published_date_iso.strftime("%Y-%m-%d")

            release_info.append(
                GithubReleaseNotes(
                    github_link=repo_url,
                    github_release_tag=latest_data.get("tag_name", None),
                    github_release_notes=latest_data.get("body", None),
                    published_date=published_date,
                )
            )

        except Exception:
            pass

    return release_info
