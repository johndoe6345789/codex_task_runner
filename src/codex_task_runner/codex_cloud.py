from __future__ import annotations

import os
import json
from typing import Iterable

import requests
from requests.cookies import RequestsCookieJar


def _parse_cookie_string(cookie_str: str) -> RequestsCookieJar:
    jar = RequestsCookieJar()
    if not cookie_str:
        return jar
    pairs = [p.strip() for p in cookie_str.split(";") if p.strip()]
    for p in pairs:
        if "=" in p:
            k, v = p.split("=", 1)
            jar.set(k.strip(), v.strip())
    return jar


def session_from_env(env_path: str | None = None) -> requests.Session:
    """Build a requests.Session using the COOKIE found in `.env` or env vars.

    `env_path` if provided will be read as a dotenv-style file. Otherwise
    environment variables are used.
    """
    sess = requests.Session()
    cookie_val = None
    extra_tokens: dict[str, str] = {}
    if env_path and os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith("#"):
                    continue
                if ln.startswith("COOKIE=") and cookie_val is None:
                    cookie_val = ln.split("=", 1)[1]
                # capture common auth tokens if present
                if ln.startswith("__Secure-next-auth.session-token="):
                    extra_tokens["session_token"] = ln.split("=", 1)[1]
                if ln.startswith("__Host-next-auth.csrf-token="):
                    extra_tokens["csrf_token"] = ln.split("=", 1)[1]
                if ln.startswith("__Secure-next-auth.callback-url="):
                    extra_tokens.setdefault("callback_url", ln.split("=", 1)[1])
    # fall back to environment variables
    if cookie_val is None:
        cookie_val = os.environ.get("COOKIE")
    extra_tokens.setdefault("session_token", os.environ.get("__Secure-next-auth.session-token") or "")
    extra_tokens.setdefault("csrf_token", os.environ.get("__Host-next-auth.csrf-token") or "")

    jar = _parse_cookie_string(cookie_val or "")
    # also set individual tokens as cookies if present
    if extra_tokens.get("session_token"):
        jar.set("__Secure-next-auth.session-token", extra_tokens["session_token"])
    if extra_tokens.get("csrf_token"):
        jar.set("__Host-next-auth.csrf-token", extra_tokens["csrf_token"])

    sess.cookies.update(jar)
    sess.headers.update({"User-Agent": "codex-task-runner/1.0"})

    # Add CSRF header if we have a csrf token (strip any pipe/hash suffix)
    csrf = extra_tokens.get("csrf_token") or ""
    if csrf:
        # cookie value sometimes encoded as "token|hash"; use left side
        token_val = csrf.split("|", 1)[0]
        sess.headers.update({"x-csrf-token": token_val})

    # If we have a session token, also provide it as an Authorization bearer (best-effort)
    sess_token = extra_tokens.get("session_token") or ""
    if sess_token:
        sess.headers.update({"Authorization": f"Bearer {sess_token}"})

    return sess


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


def poll_urls(session: requests.Session, urls: Iterable[str]) -> list[dict]:
    results: list[dict] = []
    for u in urls:
        u = u.strip()
        if not u:
            continue
        results.append(ping_url(session, u))
    return results


def save_results(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
