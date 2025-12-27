from __future__ import annotations

import json
from typing import Iterable, Optional

import requests
from .types import TaskRef


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
        repo = str(env.get("environment_label") or "")
        pr_nums = tuple()
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
