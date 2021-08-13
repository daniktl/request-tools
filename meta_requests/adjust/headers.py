from meta_requests import MetaRequest


class MetaRequestAdjustHeaders(MetaRequest):

    def __init__(self, url: str, *args, **kwargs):
        super().__init__(url, *args, **kwargs)

    def action(self):
        self.logger.info(f"Starting process for the {self.url}")
        for i, header in enumerate(self.headers.keys(), start=1):
            self.logger.info(f"Trying to send {i} headers")
            headers = {k: v for k, v in list(self.headers.items())[:i]}
            self.logger.warning(f"{self.url}, {self.body}, {headers}")
            self._last_response = self.session.request(
                method=self.method.upper(),
                url=self.url,
                data=self.body,
                headers=headers,
                cookies=self.cookies,
                proxies=self.proxies
            )
            if self.check_request_is_ok(self._last_response):
                break
