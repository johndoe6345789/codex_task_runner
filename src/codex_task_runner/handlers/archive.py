"""Archive a Codex task."""
from typing import Any

from ..etc.task_aliases import resolve_alias


def handle(args: Any, session) -> dict:
    """Archive a task by ID."""
    task_id = resolve_alias(args.task_id)
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/archive"
    
    resp = session.post(url, json={})
    
    if resp.ok:
        return {
            "task_id": task_id,
            "archived": True,
            "response": resp.json(),
        }
    else:
        return {
            "task_id": task_id,
            "archived": False,
            "error": resp.text,
            "status_code": resp.status_code,
        }
