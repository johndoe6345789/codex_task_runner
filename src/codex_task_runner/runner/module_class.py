from __future__ import annotations

from codex_task_runner.runner import runner_core, runner_io


class RunnerModule:
    """Aggregates runner core and io utilities."""

    Config = runner_core.Config
    process_tasks = staticmethod(runner_core.process_tasks)
    _process_one = staticmethod(runner_core._process_one)
    _task_pr_number = staticmethod(runner_core._task_pr_number)
    _first_open = staticmethod(runner_core._first_open)
    _maybe_create_pr = staticmethod(runner_core._maybe_create_pr)
    _pr_body = staticmethod(runner_core._pr_body)
    _is_clean = staticmethod(runner_core._is_clean)

    _fmt_task = staticmethod(runner_io._fmt_task)
    _fmt_pr = staticmethod(runner_io._fmt_pr)
    _log = staticmethod(runner_io._log)
