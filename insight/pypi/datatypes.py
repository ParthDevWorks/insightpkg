from dataclasses import dataclass


@dataclass
class RecentPackages:
    package_name: str
    package_version: str
    package_date: str
    package_github_link: str | None
    package_description: str
