from __future__ import annotations

from codex_task_runner.runner.do_process_tasks import process_tasks
from codex_task_runner.runner.runner_io import _fmt_task, _fmt_pr, _log
from codex_task_runner.etc.config_class import Config
from codex_task_runner.process.do_process_one import process_one
from codex_task_runner.process.task_pr_number import task_pr_number, _first_open, _maybe_create_pr
from codex_task_runner.process.pr_body import pr_body
from codex_task_runner.process.is_clean import is_clean


class RunnerModule:
    """Aggregates runner core and io utilities."""

    Config = Config
    process_tasks = staticmethod(process_tasks)
    _process_one = staticmethod(process_one)
    _task_pr_number = staticmethod(task_pr_number)
    _first_open = staticmethod(_first_open)
    _maybe_create_pr = staticmethod(_maybe_create_pr)
    _pr_body = staticmethod(pr_body)
    _is_clean = staticmethod(is_clean)

    _fmt_task = staticmethod(_fmt_task)
    _fmt_pr = staticmethod(_fmt_pr)
    _log = staticmethod(_log)
