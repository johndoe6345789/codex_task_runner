from __future__ import annotations

from codex_task_runner.proc.run import run
from codex_task_runner.proc.run_ok import run_ok


class ProcModule:
    """Aggregates process-run helpers."""

    run = staticmethod(run)
    run_ok = staticmethod(run_ok)
