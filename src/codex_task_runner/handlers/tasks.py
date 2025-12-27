from typing import Any, List

from ..codex.codex_tasks_list import get_tasks_list


def handle(args: Any, session) -> List[dict]:
    limit = getattr(args, "limit", 20)
    task_filter = getattr(args, "filter", "current")
    tasks = get_tasks_list(session, limit=limit, task_filter=task_filter)
    return [t.__dict__ for t in tasks]
