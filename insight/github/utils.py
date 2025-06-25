from datetime import datetime

from insight.pypi.utils import get_request
from insight.github.datatypes import GithubInfo


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

    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[-2], parts[-1]

    # GitHub API endpoint
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = get_request(api_url)

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
