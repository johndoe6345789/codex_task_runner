"""Backward-compatible shim for old module location.

Tests and external code import `codex_task_runner.codex_json`; the implementation
now lives under the `codex` subpackage. Re-export the public symbols here.
"""

from .codex.codex_json import (
    load_tasks,
    parse_tasks,
    parse_item,
)

__all__ = ["load_tasks", "parse_tasks", "parse_item"]
