"""Compatibility shim re-exporting types from the `etc` subpackage.

Older imports expect `codex_task_runner.types`; forward to `etc.types`.
"""

from __future__ import annotations

from typing import Any

from .task_ref import TaskRef
from .pull_request import PullRequest
from .merge_method import MergeMethod

# Lightweight JSON type alias used across the codebase.
Json = dict[str, Any]

__all__ = ["TaskRef", "PullRequest", "Json", "MergeMethod"]
