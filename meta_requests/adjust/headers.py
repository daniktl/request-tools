from meta_requests import MetaRequest


class MetaRequestAdjustHeaders(MetaRequest):

    def __init__(self, url: str, *args, **kwargs):
        super().__init__(url, *args, **kwargs)

    def action(self):
        self.logger.info(f"Starting process for the {self.url}")
        headers = {}
        for i, header in enumerate(self.headers.keys(), start=1):
            self.logger.info(f"Trying to send {i} headers")
            headers[header] = self.headers[header]
            self._last_response = self.session.request(
                self.method.upper(),
                url=self.url,
                headers=headers,
                proxies=self.proxies
            )
            if self._last_response.ok:
                self.logger.info(f"Found working set of headers: {headers}")
                break
