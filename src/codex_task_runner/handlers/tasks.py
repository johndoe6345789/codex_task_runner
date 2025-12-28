from typing import Any, List

from ..codex.codex_tasks_list import get_tasks_list
from ..etc.task_aliases import update_aliases


def handle(args: Any, session) -> List[dict]:
    limit = getattr(args, "limit", 20)
    task_filter = getattr(args, "filter", "current")
    tasks = get_tasks_list(session, limit=limit, task_filter=task_filter)
    
    # Convert to dicts
    task_dicts = [t.__dict__ for t in tasks]
    
    # Normalize task ID field for alias cache (some have 'task_id', some have 'id')
    for t in task_dicts:
        if "task_id" in t and "id" not in t:
            t["id"] = t["task_id"]
    
    # Update alias cache and add aliases to output
    cache = update_aliases(task_dicts)
    for t in task_dicts:
        task_id = t.get("id") or t.get("task_id", "")
        alias = cache["reverse"].get(task_id)
        if alias:
            t["_alias"] = alias
    
    return task_dicts
