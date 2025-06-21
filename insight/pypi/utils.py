import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from insight.pypi.datatypes import RecentPackages


RSS_FEED_URL = "https://pypi.org/rss/updates.xml"


def get_request(url: str) -> requests.Response | None:
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise Exception(
            f"Failed to fetch XML Content. Status Code is {response.status_code}"
        )


def get_pypi_packages_uploaded_today() -> list[RecentPackages]:
    data = []
    response = get_request(RSS_FEED_URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//item"):
        title = item.find("title").text
        description = item.find("description").text
        xml_date = item.find("pubDate").text
        package_name, package_version = title.split()

        github_link = get_github_link(package_name, package_version)

        parsed_datetime = datetime.strptime(xml_date, "%a, %d %b %Y %H:%M:%S %Z")
        # Extract only the date part
        date = parsed_datetime.date().isoformat()

        data.append(
            RecentPackages(
                package_name=package_name,
                package_version=package_version,
                package_date=date,
                package_github_link=github_link,
                package_description=description,
            )
        )

    return data


def get_github_link(package_name: str, package_version: str) -> str | None:
    url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    response = requests.get(url)

    response_dict = response.json()
    package_info = response_dict["info"]

    if package_info.get("project_urls"):
        if package_info["project_urls"].get("Homepage"):
            return package_info["project_urls"].get("Homepage")
    return None


# CLI Testing Purpose Only
if __name__ == "__main__":
    data = get_pypi_packages_uploaded_today()
    print(data)
