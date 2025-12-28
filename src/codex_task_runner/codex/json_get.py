from __future__ import annotations

from typing import Optional

from ..etc.log import log


def _json_get(session, url: str, **kwargs) -> Optional[dict]:
    import sys
    log.debug(f"HTTP GET {url}")
    print(f"DEBUG _json_get: cookies={len(session.cookies)}", file=sys.stderr)
    print(f"DEBUG _json_get: headers={list(session.headers.keys())}", file=sys.stderr)
    try:
        r = session.get(url, **kwargs)
        log.debug(f"HTTP {r.status_code} {len(r.content)} bytes")
        print(f"DEBUG _json_get: status={r.status_code}", file=sys.stderr)
        if r.status_code >= 400:
            print(f"DEBUG _json_get: response={r.text[:500]}", file=sys.stderr)
        r.raise_for_status()
        data = r.json()
        log.debug(f"HTTP JSON keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        return data
    except Exception as e:
        log.error(f"HTTP GET failed: {e}")
        return None
