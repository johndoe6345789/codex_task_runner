from __future__ import annotations

from typing import List

from .json_get import _json_get
from codex_task_runner.types import TaskRef


def get_tasks_list(session, limit: int = 20, task_filter: str = "current") -> List[TaskRef]:
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
