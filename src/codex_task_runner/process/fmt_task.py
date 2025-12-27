from __future__ import annotations

from ..types import TaskRef


def fmt_task(t: TaskRef) -> str:
    return (
        f"TASK {t.task_id}\n"
        f"  title={t.title}\n"
        f"  repo={t.repo} base={t.base_branch} prs={list(t.pr_numbers)}\n"
    )
