"""Handler for user settings."""
from typing import Any

from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """Get Codex user settings."""
    url = "https://chatgpt.com/backend-api/wham/settings/user"
    return _json_get(session, url)
