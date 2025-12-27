from __future__ import annotations

from codex_task_runner.process import process_format, process_one


class ProcessModule:
    """Aggregates processing helpers for task processing."""

    fmt_task = staticmethod(process_format.fmt_task)
    fmt_pr = staticmethod(process_format.fmt_pr)

    process_one = staticmethod(process_one.process_one)
    _task_pr_number = staticmethod(process_one._task_pr_number)
    _first_open = staticmethod(process_one._first_open)
    _maybe_create_pr = staticmethod(process_one._maybe_create_pr)
    _pr_body = staticmethod(process_one._pr_body)
    _is_clean = staticmethod(process_one._is_clean)
    _log = staticmethod(process_one._log)
