from __future__ import annotations

from codex_task_runner.gh.get_pr import get_pr
from codex_task_runner.gh.pr_exists_open import pr_exists_open
from codex_task_runner.gh.create_pr import create_pr
from codex_task_runner.etc.find_head_branch import find_head_branch
from codex_task_runner.types import TaskRef
from codex_task_runner.etc.config_class import Config
from .pr_body import pr_body


def task_pr_number(cfg: Config, t: TaskRef) -> int | None:
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
    body = pr_body(t.task_id)
    return create_pr(
        repo=t.repo,
        base=t.base_branch,
        head=head,
        title=t.title,
        body=body,
        draft=False,
        dry_run=cfg.dry_run,
    )
