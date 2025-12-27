from __future__ import annotations

import requests


def ping_url(session: requests.Session, url: str, timeout: float = 10.0) -> dict:
    try:
        r = session.get(url, timeout=timeout)
        return {
            "url": url,
            "status_code": r.status_code,
            "ok": r.ok,
            "text_snippet": (r.text[:1024] if r.text else ""),
        }
    except Exception as e:
        return {"url": url, "error": str(e)}
