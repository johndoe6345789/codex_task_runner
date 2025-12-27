from __future__ import annotations

import os
from typing import Optional

from .codex_parse_cookie import parse_cookie_string


def session_from_env(env_path: str | None = None) -> "requests.Session":
    import requests

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
                if ln.startswith("__Secure-next-auth.session-token="):
                    extra_tokens["session_token"] = ln.split("=", 1)[1]
                if ln.startswith("__Host-next-auth.csrf-token="):
                    extra_tokens["csrf_token"] = ln.split("=", 1)[1]
                if ln.startswith("__Secure-next-auth.callback-url="):
                    extra_tokens.setdefault("callback_url", ln.split("=", 1)[1])
                if ln.startswith("BEARER=") or ln.startswith("BEARER_TOKEN=") or ln.startswith("AUTHORIZATION=") or ln.startswith("ACCESS_TOKEN="):
                    k, v = ln.split("=", 1)
                    v = v.strip()
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                    extra_tokens.setdefault("bearer", v)
    if cookie_val is None:
        cookie_val = os.environ.get("COOKIE")
    extra_tokens.setdefault("session_token", os.environ.get("__Secure-next-auth.session-token") or "")
    extra_tokens.setdefault("csrf_token", os.environ.get("__Host-next-auth.csrf-token") or "")
    extra_tokens.setdefault("bearer", os.environ.get("BEARER") or os.environ.get("BEARER_TOKEN") or os.environ.get("AUTHORIZATION") or os.environ.get("ACCESS_TOKEN") or "")

    jar = parse_cookie_string(cookie_val or "")
    if extra_tokens.get("session_token"):
        jar.set("__Secure-next-auth.session-token", extra_tokens["session_token"])
    if extra_tokens.get("csrf_token"):
        jar.set("__Host-next-auth.csrf-token", extra_tokens["csrf_token"])

    sess.cookies.update(jar)
    sess.headers.update({"User-Agent": "codex-task-runner/1.0"})

    csrf = extra_tokens.get("csrf_token") or ""
    if csrf:
        token_val = csrf.split("|", 1)[0]
        sess.headers.update({"x-csrf-token": token_val})

    bearer_val = extra_tokens.get("bearer") or ""
    if bearer_val:
        if bearer_val.lower().startswith("bearer "):
            auth_header = bearer_val
        else:
            auth_header = f"Bearer {bearer_val}"
        sess.headers.update({"Authorization": auth_header})
    else:
        sess_token = extra_tokens.get("session_token") or ""
        if sess_token:
            sess.headers.update({"Authorization": f"Bearer {sess_token}"})

    return sess
