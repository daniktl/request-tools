from typing import Dict, List, Optional


def response_detect_blocking_messages(text: str, blocking_messages: List[str]) -> Optional[str]:
    """Check if page contains blocking message. Returns message if detected."""
    for message in blocking_messages:
        if message in text:
            return message
    return None


def generate_proxy_dict(proxy_str: str) -> Dict[str, str]:
    return {
        "http": proxy_str,
        "https": proxy_str
    }
