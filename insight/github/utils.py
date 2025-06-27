from datetime import datetime
import re
from typing import Callable

from insight.config import REQUEST_TOKEN
from insight.pypi.utils import get_request
from insight.pypi.datatypes import RecentPackages
from insight.github.datatypes import GithubInfo, GithubReleaseNotes

TIMEZONE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _get_owner_info(repo_url: str) -> tuple[str, str]:
    """
    Fetches and returns owner and repo_name information about a GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        owner (str): Owner of the Github Repository.
        repo (str): Repo of the Github Repository.

    Raises:
        ValueError: If the provided URL is invalid.
    """

    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)

    owner, repo = match.group(1), match.group(2)
    if owner is None or repo is None:
        raise ValueError(f"Owner :{owner} is Repo:{repo} is not correct")

    return owner, repo


def get_repo_info(repo_url: str) -> GithubInfo:
    """
    Fetches and returns information about a GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        GithubInfo: An object containing detailed information about the repository.

    Raises:
        ValueError: If the provided URL is invalid.
    """

    owner, repo = _get_owner_info(repo_url=repo_url)

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = get_request(api_url, auth=("username", REQUEST_TOKEN))

    data = response.json()

    created_date_iso = datetime.strptime(data.get("created_at"), TIMEZONE_FORMAT)
    created_date = created_date_iso.strftime("%Y-%m-%d")

    last_updated_iso = datetime.strptime(data.get("updated_at"), TIMEZONE_FORMAT)
    last_updated_date = last_updated_iso.strftime("%Y-%m-%d")

    return GithubInfo(
        github_link=repo_url,
        stars=int(data.get("stargazers_count", 0)),
        watchers=int(data.get("subscribers_count", 0)),
        forks=int(data.get("forks_count", 0)),
        open_issues=int(data.get("open_issues_count", 0)),
        created_date=created_date,
        last_updated_date=last_updated_date,
        license=data.get("license").get("name", None) if data.get("license") else None,
    )


def get_release_notes_info(repo_url: str) -> GithubReleaseNotes:
    """
    Fetches and returns Release Notes Information about a GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        GithubReleaseNotes: An object containing detailed release notes information about the repository.

    Raises:
        ValueError: If the provided URL is invalid.
    """

    owner, repo = _get_owner_info(repo_url=repo_url)

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    response = get_request(api_url, auth=("username", REQUEST_TOKEN))

    data = response.json()
    latest_data = data[0]

    published_date_iso = datetime.strptime(
        latest_data.get("published_at"), TIMEZONE_FORMAT
    )
    published_date = published_date_iso.strftime("%Y-%m-%d")

    return GithubReleaseNotes(
        github_link=repo_url,
        github_release_tag=latest_data.get("tag_name", None),
        github_release_notes=latest_data.get("body", None),
        published_date=published_date,
    )


def github_repos_metadata(
    packages: list[RecentPackages],
    callback_func: Callable[str, GithubInfo | GithubReleaseNotes],
) -> list[GithubInfo] | list[GithubReleaseNotes]:
    """
    Retrieves GitHub Repo Metadata Info for PyPI packages.

    Args:
        packages (list[RecentPackages]): A list of RecentPackages dataclass.

    Returns:
        output (list[GithubInfo] | list[GithubReleaseNotes]) : A list of GithubInfo objects or list of GithubReleaseNotes.

    """

    output = set()

    for item in packages:
        if item.package_github_link:
            try:
                repo_info = callback_func(repo_url=item.package_github_link)
                output.add(repo_info)
            except Exception:
                pass

    return list(output)
