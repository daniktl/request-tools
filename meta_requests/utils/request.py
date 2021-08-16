from typing import List, Optional


def response_detect_blocking_messages(
        text: str, blocking_messages: List[str]
) -> Optional[str]:
    """Method to check whether any of blocking messages appears in the response text.

    :param text: response text
    :param blocking_messages: list of potential blocking messages for search

    :return: first detected blocking message if exists
    """
    return next((message for message in blocking_messages if message in text), None)
