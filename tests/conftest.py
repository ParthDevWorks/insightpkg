from types import SimpleNamespace
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def data_root():
    return Path(__file__).parent.resolve() / "data"


@pytest.fixture()
def mock_response():
    def fn(content: bytes):
        return SimpleNamespace(status_code=200, content=content)

    return fn
