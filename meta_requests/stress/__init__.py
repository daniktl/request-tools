import random
import time

from tqdm import tqdm

from meta_requests import MetaRequest
from meta_requests.decorators import disable_warnings


class MetaRequestStressTest(MetaRequest):

    number_of_iterations: int
    sleep_time: int

    def __init__(self, url: str, number_of_iterations: int = 100, sleep_time: int = None, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
        self.number_of_iterations = number_of_iterations
        self.sleep_time = sleep_time

    @disable_warnings
    def action(self):
        self.logger.info(f"Starting process for the {self.url}")
        bar = tqdm(range(self.number_of_iterations))
        for i in bar:
            try:
                self._last_response = self.session.request(
                    self.method.upper(), url=self.url, headers=self.headers, proxies=self.proxies
                )
                bar.set_description(f"SUCCESS: Request {i} responded with the status code {self._last_response.status_code}")
            except Exception as exp:
                bar.set_description(f"FAILED: Request {i} failed with {exp.__class__.__name__}")

            if self.sleep_time:
                time.sleep(random.uniform(0, self.sleep_time))


