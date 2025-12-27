"""Handler for usage stats."""
from typing import Any

from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """Get Codex usage stats."""
    url = "https://chatgpt.com/backend-api/wham/usage"
    return _json_get(session, url)
