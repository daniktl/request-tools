import pytest

from meta_requests import MetaRequest


@pytest.fixture()
def meta_request():
    return MetaRequest("https://example.com")
