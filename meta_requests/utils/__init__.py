from typing import List, Optional


def response_detect_blocking_messages(text: str, blocking_messages: List[str]) -> Optional[str]:
    """Check if page contains blocking message. Returns message if detected."""
    for message in blocking_messages:
        if message in text:
            return message
    return None
