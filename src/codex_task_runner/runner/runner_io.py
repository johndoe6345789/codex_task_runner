from __future__ import annotations

from codex_task_runner.etc.append_text import append_text
from codex_task_runner.etc.default_run_dir import default_run_dir
from codex_task_runner.types import TaskRef, PullRequest


def _fmt_task(t: TaskRef) -> str:
    return (
        f"TASK {t.task_id}\n"
        f"  title={t.title}\n"
        f"  repo={t.repo} base={t.base_branch} prs={list(t.pr_numbers)}\n"
    )


def _fmt_pr(pr: PullRequest) -> str:
    return (
        f"PR #{pr.number}: {pr.title}\n"
        f"  url={pr.url}\n"
        f"  author={pr.author} mergeable={pr.mergeable} checks={pr.checks_state}\n"
    )


def _log(cfg, msg: str) -> None:
    append_text(cfg.output_dir / "run.log", msg)
