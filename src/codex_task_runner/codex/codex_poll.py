from __future__ import annotations

from typing import Iterable

from .codex_ping import ping_url


def poll_urls(session, urls: Iterable[str]) -> list[dict]:
    results: list[dict] = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        results.append(ping_url(session, u))
    return results
