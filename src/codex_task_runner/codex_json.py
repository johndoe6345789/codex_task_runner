from __future__ import annotations

import json
from typing import Any

from .types import TaskRef, Json


def load_tasks(raw: str) -> list[TaskRef]:
    obj = json.loads(raw)
    return parse_tasks(obj)


def parse_tasks(obj: Json) -> list[TaskRef]:
    items = obj.get("items") or []
    return [parse_item(i) for i in items if isinstance(i, dict)]


def parse_item(item: Json) -> TaskRef:
    ts = item.get("task_status_display") or {}
    repo = str(ts.get("environment_label") or "").strip()
    base = str(ts.get("branch_name") or "main").strip()
    prs = tuple(_extract_pr_numbers(item.get("pull_requests")))
    return TaskRef(
        task_id=str(item.get("id") or ""),
        title=str(item.get("title") or ""),
        repo=repo,
        base_branch=base,
        pr_numbers=prs,
    )


def _extract_pr_numbers(pull_requests: Any) -> list[int]:
    if not isinstance(pull_requests, list):
        return []
    nums: list[int] = []
    for prwrap in pull_requests:
        n = _extract_one(prwrap)
        if n is not None:
            nums.append(n)
    return nums


def _extract_one(prwrap: Any) -> int | None:
    if not isinstance(prwrap, dict):
        return None
    pr = prwrap.get("pull_request")
    if not isinstance(pr, dict):
        return None
    n = pr.get("number")
    return int(n) if isinstance(n, int) else None
