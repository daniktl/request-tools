import logging
import sys
from typing import Dict, List, Optional

import requests

from meta_requests.config import Config
from meta_requests.utils import response_detect_blocking_messages


class ProxyNotEnoughParamsError(Exception):
    pass


class BadUrlError(Exception):
    pass


class NoLastResponseError(Exception):
    pass


class MetaRequest:
    url: str = None
    proxies: dict = None
    _initial_headers: list = None
    headers: dict = None
    additional_proxy: dict = {}
    logger: logging.Logger
    blocking_messages: List[str] = []

    _last_response: Optional[requests.Response] = None
    save_response_path: str
    _default_save_response_path = "request_adjust.html"

    exclude_headers = ["cookie"]

    def __init__(
            self,
            url: str,
            method: str = "GET",
            proxies: dict = None,
            save_response_path: str = None,
    ):
        if "http" not in url:
            raise BadUrlError
        self.url = url
        self.method = method
        self.proxies = proxies
        self.save_response_path = save_response_path or self._default_save_response_path
        self._init_request_session()
        self._init_logger()

    def _init_request_session(self):
        """Create session and set session params based on configuration"""
        self.session = requests.Session()
        self.session.verify = Config.allow_insecure_connections  # for proxies using verify could raise SSLError
        self.session.proxies = self.proxies

    def _init_logger(self):
        """Initialize logger with output to the stdout"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def add_proxy(
            self,
            host: str,
            port: int,
            username: str = None,
            password: str = None,
            token: str = None,
            proxy_headers: Dict[str, str] = None
    ):
        """Generate proxy config based on proxy details and credentials and add it to the session."""
        if not (username and password) and not token:
            raise ProxyNotEnoughParamsError
        if username and password:
            proxy_auth = f"{username}:{password}"
        else:
            proxy_auth = f"{token}:"
        proxy_string = f"http://{proxy_auth}@{host}:{port}"
        self.proxies = {
            "http": proxy_string,
            "https": proxy_string
        }
        if isinstance(proxy_headers, dict):
            self.additional_proxy.update(proxy_headers)
        self.logger.info(f"Proxy {host} has been added to the session.")

    def add_initial_headers(self, initial_headers: list):
        """Add headers and convert them from the browser format to requests format"""
        self._initial_headers = initial_headers
        self.headers = {}
        for header in initial_headers:
            if header["name"] not in self.exclude_headers:
                header_name: str = header["name"]
                header_name = header_name[1:] if header_name.startswith(":") else header_name
                self.headers[header_name] = header["value"]

    def set_headers(self, key, value):
        self.headers[key] = value

    def save_response(self):
        if not self._last_response:
            raise NoLastResponseError
        with open(self.save_response_path, "w") as f:
            f.write(self._last_response.text)
        self.logger.info(f"Response saved to the {self.save_response_path}")

    def action(self):
        raise NotImplementedError

    def check_request_is_ok(self, response: requests.Response) -> bool:
        if not response.ok:
            self.logger.warning(f"FAILED: Request returned status code {response.status_code}.")
            return False
        detected_message = response_detect_blocking_messages(response.text, self.blocking_messages)
        if detected_message:
            self.logger.warning(f"FAILED: Request got blocked with a message {detected_message}.")
            return False
        self.logger.info(f"SUCCESS: Request passed with status code {response.status_code}")
        return True
