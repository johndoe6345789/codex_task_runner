"""Archive a Codex task."""
from .json_post import json_post


def archive_task(session, task_id: str) -> dict:
    """Archive a task by ID.
    
    Args:
        session: Codex session with auth
        task_id: Task ID to archive
        
    Returns:
        dict with {"success": True} on success
    """
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/archive"
    return json_post(session, url, {})
