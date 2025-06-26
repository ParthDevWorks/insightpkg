from datetime import datetime
import re

from insight.config import REQUEST_TOKEN
from insight.pypi.utils import get_request
from insight.pypi.datatypes import RecentPackages
from insight.github.datatypes import GithubInfo


def _get_repo_info(repo_url: str) -> GithubInfo:
    """
    Fetches and returns information about a GitHub repository.

    Args:
        repo_url (str): The URL of the GitHub repository.

    Returns:
        GithubInfo: An object containing detailed information about the repository.

    Raises:
        ValueError: If the provided URL is invalid.
    """

    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)

    owner, repo = match.group(1), match.group(2)
    if owner is None or repo is None:
        raise ValueError(f"Owner :{owner} is Repo:{repo} is not correct")

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = get_request(api_url, auth=("username", REQUEST_TOKEN))

    data = response.json()

    created_date_iso = datetime.strptime(data.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
    created_date = created_date_iso.strftime("%Y-%m-%d")

    last_updated_iso = datetime.strptime(data.get("updated_at"), "%Y-%m-%dT%H:%M:%SZ")
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


def github_repos_metadata(packages: list[RecentPackages]) -> list[GithubInfo]:
    """
    Retrieves GitHub Repo Metadata Info for PyPI packages.

    Args:
        packages (list[RecentPackages]): A list of RecentPackages dataclass.

    Returns:
        list[GithubInfo]: A list of GithubInfo objects containing GitHub repository information.

    """

    output = set()

    for item in packages:
        if item.package_github_link:
            try:
                repo_info = _get_repo_info(repo_url=item.package_github_link)
                output.add(repo_info)
            except Exception:
                pass

    return list(output)
