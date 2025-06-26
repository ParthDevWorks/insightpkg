import pytest

from insight.pypi.utils import get_pypi_packages_uploaded_today, get_github_link
from insight.pypi.datatypes import RecentPackages


def test_get_pypi_packages_uploaded_today(monkeypatch, data_root, mock_response):

    with open(data_root / "mock_response_rss_feed.xml", "r", encoding="utf-8") as f:
        xml_string = f.read()
    xml_content = xml_string.encode("utf-8")

    def mock_rss(url, auth):
        return mock_response(xml_content)

    def mock_github_link(name, version):
        return None

    monkeypatch.setattr(
        "insight.pypi.utils.requests.get",
        mock_rss,
    )

    monkeypatch.setattr(
        "insight.pypi.utils.get_github_link",
        mock_github_link,
    )

    actual_result = get_pypi_packages_uploaded_today()

    expected_result = [
        RecentPackages(
            package_name="Package1",
            package_version="1.0",
            package_upload_date="2025-06-21",
            package_upload_time="15:03:55+0000",
            package_description="Descriptioon 1",
            package_github_link=None,
        ),
        RecentPackages(
            package_name="Package2",
            package_version="2.0",
            package_upload_date="2025-06-21",
            package_upload_time="10:03:55+0000",
            package_description="Descriptioon 2",
            package_github_link=None,
        ),
    ]

    assert actual_result == expected_result


@pytest.mark.parametrize(
    "package_name, package_version, mock_response, expected_github_link",
    [
        (
            "Owner1",
            "Version 1",
            {
                "info": {
                    "project_urls": {"Homepage": "https://github.com/Owner1/reponame"}
                }
            },
            "https://github.com/Owner1/reponame",
        ),
        ("Owner2", "Version 2", {"info": {"project_urls": {}}}, None),
        ("Owner3", "Version 3", {"info": {}}, None),
    ],
    ids=[
        "Github Link Present",
        "'Homepage' Key Not Present",
        "'project_urls' Key Not Present",
    ],
)
def test_get_github_link(
    monkeypatch, package_name, package_version, mock_response, expected_github_link
):
    class MockResponse:
        def json(self):
            return mock_response

    def mock_get_request(url, auth):
        return MockResponse()

    monkeypatch.setattr(
        "insight.pypi.utils.requests.get",
        mock_get_request,
    )

    actual_github_link = get_github_link(package_name, package_version)
    assert expected_github_link == actual_github_link
