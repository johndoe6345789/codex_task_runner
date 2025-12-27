from __future__ import annotations

from codex_task_runner.proc import proc_run


class ProcModule:
    """Aggregates process-run helpers."""

    run = staticmethod(proc_run.run)
    run_ok = staticmethod(proc_run.run_ok)
