from dataclasses import dataclass


@dataclass
class RecentPackages:
    package_name: str
    package_version: str
    package_upload_date: str
    package_upload_time: str
    package_github_link: str | None
    package_description: str

    def as_tuple(self) -> tuple:
        return (
            self.package_name,
            self.package_version,
            self.package_upload_date,
            self.package_upload_time,
            self.package_github_link,
            self.package_description,
        )
