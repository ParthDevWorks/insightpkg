import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import logging

import requests

from insight.pypi.datatypes import RecentPackages


RSS_FEED_URL = "https://pypi.org/rss/updates.xml"

logger = logging.getLogger(__name__)


def get_request(url: str, auth: tuple | None = None) -> requests.Response | None:
    """
    Sends a GET request to the specified URL and returns the response if successful.

    Args:
        url (str): The URL to send the request to.
        auth (tuple | None): Auth token to Authenticate User.

    Returns:
        requests.Response | None: The response object if the request was successful, otherwise None.

    Raises:
        Exception: If the request fails and the status code is not 200.
    """

    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        logger.debug(f"GET request to {url!r} completed successfully.")
        return response
    else:
        logger.error(
            f"GET request to {url!r} failed with response code:{response.status_code!r}."
        )
        raise Exception(
            f"Failed to fetch XML Content. Status Code is {response.status_code}"
        )


def get_pypi_packages_uploaded_today() -> list[RecentPackages]:
    """
    Retrieves recently uploaded PyPI packages from the RSS feed.

    This function parses the RSS feed, extracts relevant information about newly uploaded packages,
    and returns them as a list of RecentPackages.

    Returns:
        list[RecentPackages]: A list of Recently Uploaded Packages objects containing information about newly uploaded packages.

    Note:
        This function relies on the PyPI RSS feed being available and correctly formatted.
    """

    data = []
    response = get_request(RSS_FEED_URL)
    root = ET.fromstring(response.content)

    for item in root.findall(".//item"):
        try:
            title = item.find("title").text
            description = item.find("description").text
            xml_date = item.find("pubDate").text
            package_name, package_version = title.split()

            github_link = get_github_link(package_name, package_version)

            parsed_datetime = datetime.strptime(xml_date, "%a, %d %b %Y %H:%M:%S %Z")

            # Attach UTC timezone manually
            parsed_datetime = parsed_datetime.replace(tzinfo=timezone.utc)

            # Extract only the date part
            date = parsed_datetime.date().isoformat()
            time = parsed_datetime.strftime("%H:%M:%S%z")

            data.append(
                RecentPackages(
                    package_name=package_name,
                    package_version=package_version,
                    package_upload_date=date,
                    package_upload_time=time,
                    package_github_link=github_link,
                    package_description=description,
                )
            )

        except Exception:
            pass

    return data


def get_github_link(package_name: str, package_version: str) -> str | None:
    """
    Attempts to retrieve the GitHub link for a given PyPI package version.

    Args:
        package_name (str): The name of the PyPI package.
        package_version (str): The version of the PyPI package.

    Returns:
        str | None: The GitHub link if found, otherwise None.

    Note:
        This function relies on the PyPI JSON API being available and correctly formatted.
    """

    url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    response = get_request(url)

    response_dict = response.json()
    package_info = response_dict["info"]

    if package_info.get("project_urls"):
        if package_info["project_urls"].get("Homepage"):
            return package_info["project_urls"].get("Homepage")
    return None
