from __future__ import annotations

from codex_task_runner.codex.json_get import _json_get
from codex_task_runner.codex.json_post import _json_post
from codex_task_runner.codex.extract_pr_numbers import extract_pr_numbers, _extract_one
from codex_task_runner.codex.parse_tasks import parse_tasks
from codex_task_runner.codex.load_tasks import load_tasks


class CodexModule:
    """Aggregates common codex helpers into a single class."""

    _json_get = staticmethod(_json_get)
    _json_post = staticmethod(_json_post)

    extract_pr_numbers = staticmethod(extract_pr_numbers)
    _extract_one = staticmethod(_extract_one)

    parse_tasks = staticmethod(parse_tasks)
    load_tasks = staticmethod(load_tasks)
