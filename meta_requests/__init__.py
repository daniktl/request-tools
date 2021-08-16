import logging
import random
import sys
from typing import Dict, List, Optional, Union

from requests import Response, Session
from requests.cookies import RequestsCookieJar

from meta_requests.config import Config
from meta_requests.utils import generate_proxy_dict
from meta_requests.utils.decorators import disable_warnings
from meta_requests.utils.exceptions import (
    BadUrlError,
    ProxyNotEnoughParamsError,
    NoLastResponseError,
)
from meta_requests.utils.request import response_detect_blocking_messages


class MetaRequest:
    """Base Meta Request class to initiate all basic methods
    to initiate request with required parameters: proxies, cookies, headers and etc.
    """

    url: str = None
    proxy_pool: List[str] = None
    _initial_headers: list = None
    _initial_cookies: list = None
    headers: dict = None
    cookies: RequestsCookieJar = None
    logger: logging.Logger = None
    blocking_messages: List[str] = None
    _last_response: Optional[Response] = None
    save_response_path: str = None

    _default_save_response_path = "request_adjust.html"
    exclude_headers = [
        "cookie"
    ]  # cookies has to be initiated as cookies, not headers attribute

    def __init__(
            self,
            url: str,
            method: str = "GET",
            body: str = None,
            proxy_pool: List[str] = None,
            save_response_path: str = None,
            blocking_messages: Optional[List] = None,
    ) -> None:
        if not url.startswith("http"):
            raise BadUrlError
        self.url = url
        self.method = method
        self.body = body
        self.headers = {}
        self.cookies = RequestsCookieJar()
        self.proxy_pool = proxy_pool or []
        self.save_response_path = save_response_path or self._default_save_response_path
        self.blocking_messages = blocking_messages or []
        self._init_request_session()
        self._init_logger()

    def _init_request_session(self) -> None:
        """Create session and set session params based on configuration"""
        self.session = Session()
        self.session.verify = (
            Config.allow_insecure_connections
        )  # for proxies using verify could raise SSLError
        self.session.proxies = self.get_proxy()

    def _init_logger(self) -> None:
        """Initialize logger with output to the stdout"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_proxy(self) -> Optional[Dict]:
        """Get random proxy from the proxy pool if any proxy was added"""
        return (
            generate_proxy_dict(random.choice(self.proxy_pool))
            if self.proxy_pool
            else None
        )

    def add_authenticated_proxy(
            self,
            host: str,
            port: int,
            username: str = None,
            password: str = None,
            token: str = None,
            proxy_headers: Dict[str, str] = None,
    ) -> None:
        """Generate proxy config based on proxy details and credentials and add it to the session.

        :param host: proxy provider host
        :param port: proxy provider port
        :param username: your proxy credentials (1) - username
        :param password: your proxy credentials (1) - password
        :param token: your proxy credentials (2) - token
        :param proxy_headers: additional, proxy-specific headers
        """
        if not (username and password or token):
            raise ProxyNotEnoughParamsError
        if username and password:
            proxy_auth = f"{username}:{password}"
        else:
            proxy_auth = f"{token}:"
        proxy_string = f"http://{proxy_auth}@{host}:{port}"
        self.proxy_pool.append(proxy_string)
        if isinstance(proxy_headers, dict):
            self.headers.update(proxy_headers)
        self.logger.info(f"Proxy {host} has been added to the session.")

    def set_initial_headers(self, initial_headers: list) -> None:
        """Add headers and convert them from the HAR to the python requests format

        :param initial_headers: HAR formatted headers
        """
        self._initial_headers = initial_headers
        self.headers = {}
        for header in initial_headers:
            if header["name"] not in self.exclude_headers:
                header_name: str = header["name"]
                header_name = (
                    header_name[1:] if header_name.startswith(":") else header_name
                )
                self.headers[header_name] = header["value"]

    def set_initial_cookies(self, initial_cookies: list) -> None:
        """Add cookies and convert the from browser format to the dict object"""
        self._initial_cookies = initial_cookies
        self.cookies = RequestsCookieJar()
        # converts HAR cookies to the CookieJar that Python requests module is using
        for cookie in initial_cookies:
            self.cookies.set(
                name=cookie["name"],
                value=cookie["value"],
                domain=cookie.get("domain"),
                path=cookie.get("path"),
                secure=cookie.get("secure"),
                rest={"HttpOnly": cookie["httpOnly"]},
            )

    def set_header(self, key: str, value: Union[str, int, None]) -> None:
        self.headers[key] = value

    def save_response(self) -> None:
        """Method to save the last response to the file for further analytics"""
        if not self._last_response:
            raise NoLastResponseError
        with open(self.save_response_path, "w") as f:
            f.write(self._last_response.text)
        self.logger.info(f"Response saved to the {self.save_response_path}")

    @disable_warnings
    def action(self) -> None:
        """Default action, that just making a single request to the target"""
        self.logger.debug(f"{self.url}, {self.body}, {self.headers}")
        self._last_response = self.session.request(
            method=self.method.upper(),
            url=self.url,
            data=self.body,
            headers=self.headers,
            cookies=self.cookies,
            proxies=self.get_proxy(),
        )
        self.check_request_is_ok(self._last_response)

    def check_request_is_ok(self, response: Response) -> bool:
        """Method to detects whether the request was blocked.
        Returns the "blocked" flag and add some logs.

        :param response: response from the target

        :return: the "blocked" flag
        """
        detected_message = response_detect_blocking_messages(
            response.text, self.blocking_messages
        )
        if detected_message:
            self.logger.warning(
                f"FAILED: Request got blocked with a message: <{detected_message}>."
            )
            return False
        if not response.ok:
            self.logger.warning(
                f"FAILED: Request returned status code: {response.status_code}."
            )
            return False
        self.logger.info(
            f"SUCCESS: Request passed with status code: {response.status_code}"
        )
        return True
