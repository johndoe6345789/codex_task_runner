"""Fetch and filter tasks from Codex."""
from ..codex.codex_tasks_list import get_tasks_list
from .filter_tasks import filter_tasks
from ..etc.log import log


def fetch_tasks(session, limit: int, repo_filter: str | None) -> list | None:
    """Fetch tasks and filter by repo. Returns None if no tasks."""
    log.info(f"Fetching up to {limit} tasks...")
    tasks = get_tasks_list(session, limit=limit)
    
    if not tasks:
        log.error("No tasks found")
        return None
    
    tasks = filter_tasks(tasks, repo_filter)
    log.info(f"Found {len(tasks)} tasks" + (f" for {repo_filter}" if repo_filter else ""))
    
    if not tasks:
        log.warning("No tasks match filter")
        return None
    
    return tasks
