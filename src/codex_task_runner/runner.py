from __future__ import annotations

import pathlib
from dataclasses import dataclass

from .branch_finder import find_head_branch
from .fsutil import default_run_dir, ensure_dir, append_text
from .gh_api import (
    pr_exists_open,
    create_pr,
    get_pr,
    merge_pr,
)
from .types import MergeMethod, TaskRef, PullRequest


@dataclass(frozen=True)
class Config:
    require_checks: bool
    method: MergeMethod
    delete_branch: bool
    admin: bool
    auto: bool
    dry_run: bool
    output_dir: pathlib.Path


def process_tasks(cfg: Config, tasks: list[TaskRef]) -> None:
    ensure_dir(cfg.output_dir)
    for t in tasks:
        _process_one(cfg, t)


def _process_one(cfg: Config, t: TaskRef) -> None:
    _log(cfg, _fmt_task(t))
    prn = _task_pr_number(cfg, t)
    if prn is None:
        _log(cfg, "SKIP: no PR and could not create\n")
        return
    pr = get_pr(t.repo, prn)
    _log(cfg, _fmt_pr(pr))
    if not _is_clean(pr, cfg.require_checks):
        _log(cfg, "SKIP: not clean\n")
        return
    ok = merge_pr(
        t.repo, pr.number, cfg.method, cfg.delete_branch,
        cfg.admin, cfg.auto, cfg.dry_run,
    )
    _log(cfg, f"MERGE: {'OK' if ok else 'FAIL'}\n")


def _task_pr_number(cfg: Config, t: TaskRef) -> int | None:
    nums = [n for n in t.pr_numbers if isinstance(n, int)]
    open_pr = _first_open(t.repo, nums)
    if open_pr is not None:
        return open_pr
    return _maybe_create_pr(cfg, t)


def _first_open(repo: str, nums: list[int]) -> int | None:
    for n in nums:
        try:
            pr = get_pr(repo, n)
        except Exception:
            # If we can't fetch PR info (repo inaccessible), skip it.
            continue
        if pr.mergeable:
            return n
    return None


def _maybe_create_pr(cfg: Config, t: TaskRef) -> int | None:
    head = find_head_branch(t.repo, t.title, t.task_id)
    if head is None:
        return None
    existing = pr_exists_open(t.repo, head)
    if existing is not None:
        return existing
    body = _pr_body(t.task_id)
    return create_pr(
        repo=t.repo,
        base=t.base_branch,
        head=head,
        title=t.title,
        body=body,
        draft=False,
        dry_run=cfg.dry_run,
    )


def _pr_body(task_id: str) -> str:
    return f"\n------\n[Codex Task](https://chatgpt.com/codex/tasks/{task_id})\n"


def _is_clean(pr: PullRequest, require_checks: bool) -> bool:
    if pr.mergeable != "MERGEABLE":
        return False
    if not require_checks:
        return True
    return pr.checks_state == "SUCCESS"


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


def _log(cfg: Config, msg: str) -> None:
    append_text(cfg.output_dir / "run.log", msg)


def make_config(
    require_checks: bool,
    method: str,
    keep_branch: bool,
    admin: bool,
    auto: bool,
    dry_run: bool,
    output_dir: str | None,
) -> Config:
    out = pathlib.Path(output_dir) if output_dir else default_run_dir()
    return Config(
        require_checks=require_checks,
        method=MergeMethod(method),
        delete_branch=not keep_branch,
        admin=admin,
        auto=auto,
        dry_run=dry_run,
        output_dir=out,
    )
