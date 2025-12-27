"""Handler for current user info."""
from typing import Any

from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """Get current user info."""
    url = "https://chatgpt.com/backend-api/me"
    return _json_get(session, url)
