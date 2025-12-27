"""Compatibility wrapper re-exporting the newer processor/config modules.

The heavy lifting lives in `runner_core.py` and `etc/config.py`; keep this
module so older imports keep working.
"""

from __future__ import annotations

from .runner_core import process_tasks
from codex_task_runner.etc.config import Config, make_config

__all__ = ["Config", "process_tasks", "make_config"]
