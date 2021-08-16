from meta_requests.utils import *


def test_generate_proxy_dict():
    proxy_str = "https://127.0.0.1:8000"
    expected_output = {
        "http": proxy_str,
        "https": proxy_str
    }
    actual_output = generate_proxy_dict(proxy_str)
    assert expected_output == actual_output
