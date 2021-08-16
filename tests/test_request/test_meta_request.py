import pytest

from meta_requests import MetaRequest
from meta_requests.utils.exceptions import BadUrlError


class TestMetaRequest:

    @staticmethod
    def test_request_action_is_ok(meta_request: MetaRequest):
        """Test to check if the MetaRequest initiates correctly"""
        ok_status = meta_request.action()
        assert ok_status is None

    @staticmethod
    def test_request_raise_bad_url():
        with pytest.raises(BadUrlError):
            MetaRequest(url="bad_url")

    @staticmethod
    def test_request_correctly_adds_proxies(meta_request: MetaRequest):
        proxy_host = "xyz"
        proxy_port = 8080
        proxy_token = "123"
        expected_url = f"http://{proxy_token}:@{proxy_host}:{proxy_port}"
        expected_output = {
            "http": expected_url,
            "https": expected_url
        }
        meta_request.add_authenticated_proxy(host="xyz", port=8080, token="123")
        assert meta_request.get_proxy() == expected_output
