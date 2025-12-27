from __future__ import annotations

from typing import Any

from .etc.task_ref import TaskRef
from .etc.pull_request import PullRequest
from .etc.merge_method import MergeMethod

# Lightweight JSON type alias used across the codebase.
Json = dict[str, Any]

__all__ = ["TaskRef", "PullRequest", "Json", "MergeMethod"]
