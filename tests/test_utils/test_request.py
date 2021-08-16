from meta_requests.utils.request import *
from tests.utils import get_response_with_text


def test_response_detect_blocking_messages():
    blocked_message: str = "You got blocked"
    text = get_response_with_text(blocked_message)
    assert response_detect_blocking_messages(text, [blocked_message])
