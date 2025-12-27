from __future__ import annotations

import requests

from ..etc.log import log


def ping_url(session: requests.Session, url: str, timeout: float = 10.0) -> dict:
    log.debug(f"HTTP PING {url}")
    try:
        r = session.get(url, timeout=timeout)
        log.debug(f"HTTP {r.status_code} {len(r.content)} bytes")
        return {
            "url": url,
            "status_code": r.status_code,
            "ok": r.ok,
            "text_snippet": (r.text[:1024] if r.text else ""),
        }
    except Exception as e:
        log.error(f"HTTP PING failed: {e}")
        return {"url": url, "error": str(e)}
