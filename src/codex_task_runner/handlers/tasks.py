from typing import Any, List

from ..codex.codex_tasks_list import get_tasks_list


def handle(args: Any, session) -> List[dict]:
    tasks = get_tasks_list(session, limit=getattr(args, "limit", 20))
    return [t.__dict__ for t in tasks]
