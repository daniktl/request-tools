from typing import Iterable

from meta_requests import MetaRequest
from meta_requests.utils.exceptions import RequiredAttributeError
from meta_requests.utils.iterative import power_set


class MetaRequestAdjustHeaders(MetaRequest):
    def __init__(self, url: str, *args, **kwargs):
        super().__init__(url, *args, **kwargs)

    def action(self):
        if self.headers is None:
            raise RequiredAttributeError("Headers has to be set")
        self.logger.info(f"Starting process for the {self.url}")
        headers_power_set: Iterable = power_set(self.headers.items())
        for i, headers_set in enumerate(headers_power_set, start=1):
            print(headers_set)
            self.logger.info(
                f"Trying to send set of headers: {[x[0] for x in headers_set]}"
            )
            self._last_response = self.session.request(
                method=self.method.upper(),
                url=self.url,
                data=self.body,
                headers=dict(headers_set),
                cookies=self.cookies,
                proxies=self.get_proxy(),
            )
            if self.check_request_is_ok(self._last_response):
                self.logger.info(
                    f"Found the best working set of headers: {headers_set if headers_set else 'No headers required'}"
                )
                break
