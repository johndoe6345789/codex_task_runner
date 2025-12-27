from typing import Any

from ..codex_cloud import ping_url


def handle(args: Any, session) -> dict:
    """Ping a single URL and return the JSON-serializable result."""
    return ping_url(session, args.url)
