"""Handler for GitHub repositories."""
from typing import Any

from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """List connected GitHub repositories."""
    page = getattr(args, "page", 1)
    per_page = getattr(args, "per_page", 10)
    
    url = f"https://chatgpt.com/backend-api/wham/github/list-repositories?page={page}&per_page={per_page}"
    return _json_get(session, url)
