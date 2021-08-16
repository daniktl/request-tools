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
    def test_request_add_proxy(meta_request: MetaRequest):
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

    @staticmethod
    def test_request_set_initial_headers(meta_request: MetaRequest):
        header_key = "Accept"
        header_value = "application/json"
        har_headers = [
            {"name": header_key, "value": header_value},
        ]
        meta_request.set_initial_headers(har_headers)
        assert header_key in meta_request.headers
        assert meta_request.headers[header_key] == header_value

    @staticmethod
    def test_request_set_header(meta_request: MetaRequest):
        header_key = "Accept"
        header_value = "application/json"
        meta_request.set_header(header_key, header_value)
        assert header_key in meta_request.headers
        assert meta_request.headers[header_key] == header_value
