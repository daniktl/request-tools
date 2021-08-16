# Request Tools

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tool for adjusting requests to perform a simple web-scrapping or testing.

## Installing

To use it, be sure to install all required packages from the `requirements.txt` file.

## Usage

Example snippet to start using this module (example covers one module, the flow is similar for the rest):

```python
from meta_requests.adjust.headers import MetaRequestAdjustHeaders

meta_request = MetaRequestAdjustHeaders(url="https://www.test.com")  # Replace with target url
meta_request.add_authenticated_proxy(
    host="my.proxy.com", port=8080, username="not_a_bot", password="not_a_password"
)  # Optionally - use proxy pool to make requests
meta_request.set_initial_headers(
    [
        {
            "name": ":method",
            "value": "GET"
        },
        {
            "name": ":authority",
            "value": "www.test.com"
        },
        {
            "name": ":scheme",
            "value": "https"
        },
        {
            "name": ":path",
            "value": "/"
        },
        {
            "name": "cache-control",
            "value": "max-age=0"
        },
    ]
)  # Export headers from the dev tools
meta_request.set_header("Accept", "application/json")  # Or manually set headers
meta_request.action()  # Starts the execution. Stops when find the smallest working set of proxy
```
