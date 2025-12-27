"""Handler for environments."""
from typing import Any

from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """List Codex environments."""
    recent = getattr(args, "recent", False)
    
    if recent:
        url = "https://chatgpt.com/backend-api/wham/environments/recent"
    else:
        url = "https://chatgpt.com/backend-api/wham/environments"
    
    return _json_get(session, url)
