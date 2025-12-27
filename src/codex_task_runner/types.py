from __future__ import annotations

from typing import Any

from .merge_method import MergeMethod
from .task_ref import TaskRef
from .pull_request import PullRequest


Json = dict[str, Any]

__all__ = ["MergeMethod", "TaskRef", "PullRequest", "Json"]
