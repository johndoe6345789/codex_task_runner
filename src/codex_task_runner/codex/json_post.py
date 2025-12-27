from __future__ import annotations

from typing import Optional


def _json_post(session, url: str, data=None, **kwargs) -> Optional[dict]:
    try:
        r = session.post(url, json=data or {}, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None
