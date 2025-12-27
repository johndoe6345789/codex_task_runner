from __future__ import annotations

from codex_task_runner.gh.get_pr import get_pr
from codex_task_runner.gh.merge_pr import merge_pr
from codex_task_runner.etc.append_text import append_text
from codex_task_runner.types import TaskRef, PullRequest
from codex_task_runner.etc.config_class import Config
from .fmt_task import fmt_task
from codex_task_runner.pr.fmt_pr import fmt_pr
from codex_task_runner.pr.task_pr_number import task_pr_number
from .is_clean import is_clean


def process_one(cfg: Config, t: TaskRef) -> None:
    _log(cfg, fmt_task(t))
    prn = task_pr_number(cfg, t)
    if prn is None:
        _log(cfg, "SKIP: no PR and could not create\n")
        return
    pr = get_pr(t.repo, prn)
    _log(cfg, fmt_pr(pr))
    if not is_clean(pr, cfg.require_checks):
        _log(cfg, "SKIP: not clean\n")
        return
    ok = merge_pr(
        t.repo, pr.number, cfg.method, cfg.delete_branch,
        cfg.admin, cfg.auto, cfg.dry_run,
    )
    _log(cfg, f"MERGE: {'OK' if ok else 'FAIL'}\n")


def _log(cfg: Config, msg: str) -> None:
    append_text(cfg.output_dir / "run.log", msg)
