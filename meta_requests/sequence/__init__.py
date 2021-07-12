from http import HTTPStatus

from tqdm import tqdm

from meta_requests import MetaRequest
from meta_requests.decorators import disable_warnings


class MetaRequestSequence(MetaRequest):

    urls: list
    iterations: int

    def __init__(self, urls: list, iterations: int = 1, *args, **kwargs):
        super().__init__(url="http", *args, **kwargs)
        self.urls = urls
        self.iterations = iterations

    @disable_warnings
    def action(self):
        self.logger.info("Starting sequence process for the provided urls...")
        bar = tqdm(self.urls * self.iterations)
        for url in bar:
            try:
                self._last_response = self.session.request(
                    self.method.upper(), url=url, headers=self.headers, proxies=self.proxies
                )
                if self._last_response.status_code != HTTPStatus.OK:
                    self.logger.warning(f"Request {url} responded with the status code {self._last_response.status_code}.")
                bar.set_description(f"SUCCESS: Request {url} responded with the status code {self._last_response.status_code}")
            except Exception as exp:
                bar.set_description(f"FAILED: Request {url} failed with {exp.__class__.__name__}")
