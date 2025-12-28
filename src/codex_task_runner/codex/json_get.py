from __future__ import annotations

from typing import Optional

from ..etc.log import log


def _json_get(session, url: str, **kwargs) -> Optional[dict]:
    log.debug(f"HTTP GET {url}")
    try:
        r = session.get(url, **kwargs)
        log.debug(f"HTTP {r.status_code} {len(r.content)} bytes")
        r.raise_for_status()
        data = r.json()
        log.debug(f"HTTP JSON keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        return data
    except Exception as e:
        log.error(f"HTTP GET failed: {e}")
        return None
