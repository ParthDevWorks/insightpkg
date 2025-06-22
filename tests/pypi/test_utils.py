from insight.pypi.utils import get_pypi_packages_uploaded_today


def test_get_pypi_packages_uploaded_today(monkeypatch, data_root, mock_response):

    with open(data_root / "mock_response_rss_feed.xml", "r", encoding="utf-8") as f:
        xml_string = f.read()
    xml_content = xml_string.encode("utf-8")

    def mock_rss(url):
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

    result = get_pypi_packages_uploaded_today()

    assert len(result) == 2
    assert result[0].package_name == "Package1"
    assert result[0].package_version == "1.0"
    assert result[1].package_name == "Package2"
    assert result[1].package_version == "2.0"
