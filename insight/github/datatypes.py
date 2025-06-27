from dataclasses import dataclass


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class GithubReleaseNotes:
    github_link: str
    github_release_tag: str | None
    published_date: str
    github_release_notes: str | None

    def as_tuple(self) -> tuple:
        return (
            self.github_link,
            self.github_release_tag,
            self.published_date,
            self.github_release_notes,
        )
