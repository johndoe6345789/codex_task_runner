from __future__ import annotations

from typing import Any

from ..types import TaskRef
from .codex_parse_prs import extract_pr_numbers


def parse_item(item: Any) -> TaskRef:
    ts = item.get("task_status_display") or {}
    repo = str(ts.get("environment_label") or "johndoe6345789/metabuilder").strip()
    base = str(ts.get("branch_name") or "main").strip()
    prs = tuple(extract_pr_numbers(item.get("pull_requests")))
    return TaskRef(
        task_id=str(item.get("id") or ""),
        title=str(item.get("title") or ""),
        repo=repo,
        base_branch=base,
        pr_numbers=prs,
    )
