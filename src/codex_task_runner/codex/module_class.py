from __future__ import annotations

from codex_task_runner.codex import codex_http, codex_parse_prs, codex_parse_tasks


class CodexModule:
    """Aggregates common codex helpers into a single class."""

    _json_get = staticmethod(codex_http._json_get)
    _json_post = staticmethod(codex_http._json_post)

    extract_pr_numbers = staticmethod(codex_parse_prs.extract_pr_numbers)
    _extract_one = staticmethod(codex_parse_prs._extract_one)

    parse_tasks = staticmethod(codex_parse_tasks.parse_tasks)
    load_tasks = staticmethod(codex_parse_tasks.load_tasks)
