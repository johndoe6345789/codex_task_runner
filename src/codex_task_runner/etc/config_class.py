from __future__ import annotations

import pathlib
from dataclasses import dataclass

from .merge_method import MergeMethod


@dataclass(frozen=True)
class Config:
    require_checks: bool
    method: MergeMethod
    delete_branch: bool
    admin: bool
    auto: bool
    dry_run: bool
    output_dir: pathlib.Path
    create_followup_tasks: bool = False  # Auto-create tasks for non-mergeable PRs
