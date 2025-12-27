from __future__ import annotations

from typing import Optional


def json_get(session, url: str, **kwargs) -> Optional[dict]:
    try:
        r = session.get(url, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None
