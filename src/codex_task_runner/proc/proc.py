"""Compatibility wrapper re-exporting `proc_run` helpers.

`proc_run.py` contains the real implementations; keep this module so
imports that reference `codex_task_runner.proc` continue to work.
"""

from .proc_run import run, run_ok

__all__ = ["run", "run_ok"]
