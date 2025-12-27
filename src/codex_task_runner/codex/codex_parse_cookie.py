from __future__ import annotations

from requests.cookies import RequestsCookieJar


def parse_cookie_string(cookie_str: str) -> RequestsCookieJar:
    jar = RequestsCookieJar()
    if not cookie_str:
        return jar
    pairs = [p.strip() for p in cookie_str.split(";") if p.strip()]
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            jar.set(k.strip(), v.strip())
    return jar
