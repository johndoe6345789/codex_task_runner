from __future__ import annotations

from ..types import TaskRef, PullRequest


def fmt_task(t: TaskRef) -> str:
    return (
        f"TASK {t.task_id}\n"
        f"  title={t.title}\n"
        f"  repo={t.repo} base={t.base_branch} prs={list(t.pr_numbers)}\n"
    )


def fmt_pr(pr: PullRequest) -> str:
    return (
        f"PR #{pr.number}: {pr.title}\n"
        f"  url={pr.url}\n"
        f"  author={pr.author} mergeable={pr.mergeable} checks={pr.checks_state}\n"
    )
