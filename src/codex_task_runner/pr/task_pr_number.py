from __future__ import annotations

from codex_task_runner.types import TaskRef
from codex_task_runner.etc.config_class import Config
from .first_open import _first_open
from .maybe_create_pr import _maybe_create_pr


def task_pr_number(cfg: Config, t: TaskRef) -> int | None:
    nums = [n for n in t.pr_numbers if isinstance(n, int)]
    open_pr = _first_open(t.repo, nums)
    if open_pr is not None:
        return open_pr
    return _maybe_create_pr(cfg, t)

