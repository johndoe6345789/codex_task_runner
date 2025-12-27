from __future__ import annotations

from typing import Optional

from ..etc.log import log


def _json_post(session, url: str, data=None, **kwargs) -> Optional[dict]:
    log.debug(f"HTTP POST {url}")
    log.debug(f"HTTP body: {data}")
    try:
        r = session.post(url, json=data or {}, **kwargs)
        log.debug(f"HTTP {r.status_code} {len(r.content)} bytes")
        r.raise_for_status()
        resp = r.json()
        log.debug(f"HTTP JSON keys: {list(resp.keys()) if isinstance(resp, dict) else type(resp)}")
        return resp
    except Exception as e:
        log.error(f"HTTP POST failed: {e}")
        return None
