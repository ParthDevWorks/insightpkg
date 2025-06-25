from dataclasses import dataclass


@dataclass
class GithubInfo:
    github_link: str
    stars: int
    watchers: int
    forks: int
    open_issues: int
    created_date: str
    last_updated_date: str
    license: str | None

    def as_tuple(self) -> tuple:
        return (
            self.github_link,
            self.stars,
            self.watchers,
            self.forks,
            self.open_issues,
            self.created_date,
            self.last_updated_date,
            self.license,
        )
