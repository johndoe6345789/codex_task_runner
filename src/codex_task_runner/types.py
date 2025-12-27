from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MergeMethod(str, Enum):
    MERGE = "merge"
    SQUASH = "squash"
    REBASE = "rebase"


@dataclass(frozen=True)
class TaskRef:
    task_id: str
    title: str
    repo: str
    base_branch: str
    pr_numbers: tuple[int, ...]


@dataclass(frozen=True)
class PullRequest:
    number: int
    url: str
    title: str
    author: str
    mergeable: str
    checks_state: str | None


Json = dict[str, Any]
