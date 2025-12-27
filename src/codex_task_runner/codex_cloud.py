from __future__ import annotations

import os
import json
from typing import Iterable

import requests
from requests.cookies import RequestsCookieJar
from .types import TaskRef
from typing import Optional


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
                # capture explicit bearer/authorization tokens if present
                if ln.startswith("BEARER=") or ln.startswith("BEARER_TOKEN=") or ln.startswith("AUTHORIZATION=") or ln.startswith("ACCESS_TOKEN="):
                    k, v = ln.split("=", 1)
                    # strip surrounding quotes if present
                    v = v.strip()
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                    extra_tokens.setdefault("bearer", v)
    # fall back to environment variables
    if cookie_val is None:
        cookie_val = os.environ.get("COOKIE")
    extra_tokens.setdefault("session_token", os.environ.get("__Secure-next-auth.session-token") or "")
    extra_tokens.setdefault("csrf_token", os.environ.get("__Host-next-auth.csrf-token") or "")
    # look for common bearer env vars
    extra_tokens.setdefault("bearer", os.environ.get("BEARER") or os.environ.get("BEARER_TOKEN") or os.environ.get("AUTHORIZATION") or os.environ.get("ACCESS_TOKEN") or "")

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

    # Prefer an explicit bearer token if present, otherwise fall back to session token
    bearer_val = extra_tokens.get("bearer") or ""
    if bearer_val:
        # Accept values that already include the 'Bearer ' prefix or raw tokens
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


def _json_get(session: requests.Session, url: str, **kwargs) -> Optional[dict]:
    try:
        r = session.get(url, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _json_post(session: requests.Session, url: str, data=None, **kwargs) -> Optional[dict]:
    try:
        r = session.post(url, json=data or {}, **kwargs)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def get_tasks_list(session: requests.Session, limit: int = 20, task_filter: str = "current") -> list[TaskRef]:
    """Return a list of TaskRef objects pulled from the Codex Cloud tasks list endpoint."""
    url = f"https://chatgpt.com/backend-api/wham/tasks/list?limit={limit}&task_filter={task_filter}"
    data = _json_get(session, url)
    out: list[TaskRef] = []
    if not data:
        return out
    items = data.get("items") or data.get("results") or []
    for it in items:
        task_id = it.get("id") or it.get("task_id")
        title = it.get("title") or it.get("name") or ""
        env = it.get("task_status_display") or {}
        base = env.get("environment_label") or "main"
        # Extract repo if present in environment_label like owner/repo
        repo = str(env.get("environment_label") or "")
        pr_nums = tuple()
        # cached_pull_request_data may contain PR numbers
        cached = it.get("denormalized_metadata", {}).get("cached_pull_request_data") if isinstance(it.get("denormalized_metadata"), dict) else None
        if cached and isinstance(cached, dict):
            try:
                pr_nums = tuple(int(x) for x in (cached.get("numbers") or []))
            except Exception:
                pr_nums = tuple()
        out.append(TaskRef(task_id=str(task_id), title=str(title), repo=repo, base_branch=str(base), pr_numbers=pr_nums))
    return out


def get_task(session: requests.Session, task_id: str) -> Optional[dict]:
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}"
    return _json_get(session, url)


def get_turns(session: requests.Session, task_id: str) -> Optional[dict]:
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns"
    return _json_get(session, url)


def create_pr_for_turn(session: requests.Session, task_id: str, turn_id: str) -> Optional[dict]:
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns/{turn_id}/pr"
    return _json_post(session, url, data={})
