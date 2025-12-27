from __future__ import annotations

from codex_task_runner.process.fmt_task import fmt_task
from codex_task_runner.pr.fmt_pr import fmt_pr
from codex_task_runner.process.do_process_one import process_one, _log
from codex_task_runner.pr.task_pr_number import task_pr_number
from codex_task_runner.pr.first_open import _first_open
from codex_task_runner.pr.maybe_create_pr import _maybe_create_pr
from codex_task_runner.pr.pr_body import pr_body
from codex_task_runner.process.is_clean import is_clean


class ProcessModule:
    """Aggregates processing helpers for task processing."""

    fmt_task = staticmethod(fmt_task)
    fmt_pr = staticmethod(fmt_pr)

    process_one = staticmethod(process_one)
    _task_pr_number = staticmethod(task_pr_number)
    _first_open = staticmethod(_first_open)
    _maybe_create_pr = staticmethod(_maybe_create_pr)
    _pr_body = staticmethod(pr_body)
    _is_clean = staticmethod(is_clean)
    _log = staticmethod(_log)
