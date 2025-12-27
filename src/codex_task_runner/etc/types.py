"""Compatibility shim re-exporting types from the `etc` subpackage.

Older imports expect `codex_task_runner.types`; forward to `etc.types`.
"""

from .etc.types import (
    TaskRef,
    PullRequest,
    Json,
    MergeMethod,
)

__all__ = ["TaskRef", "PullRequest", "Json", "MergeMethod"]
