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
                self.check_request_is_ok(self._last_response)
            except Exception as exp:
                self.logger.error(f"FAILED: Request {url} failed with {exp.__class__.__name__}")
