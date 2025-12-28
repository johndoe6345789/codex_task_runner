"""Task alias cache for short task references."""
import json
from pathlib import Path
from typing import Optional

# Default cache location
CACHE_FILE = Path.home() / ".codex-task-cache.json"


def load_cache(cache_path: Path = CACHE_FILE) -> dict:
    """Load the task alias cache."""
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except (json.JSONDecodeError, IOError):
            return {"aliases": {}, "reverse": {}}
    return {"aliases": {}, "reverse": {}}


def save_cache(cache: dict, cache_path: Path = CACHE_FILE) -> None:
    """Save the task alias cache."""
    cache_path.write_text(json.dumps(cache, indent=2))


def update_aliases(tasks: list[dict], cache_path: Path = CACHE_FILE) -> dict:
    """Update aliases from a list of tasks. Returns the updated cache."""
    cache = {"aliases": {}, "reverse": {}}
    
    for i, task in enumerate(tasks, start=1):
        # Support both 'id' and 'task_id' field names
        task_id = task.get("id") or task.get("task_id", "")
        if task_id:
            alias = str(i)
            cache["aliases"][alias] = task_id
            cache["reverse"][task_id] = alias
    
    save_cache(cache, cache_path)
    return cache


def resolve_alias(task_ref: str, cache_path: Path = CACHE_FILE) -> str:
    """Resolve a task reference (alias or full ID) to the full task ID."""
    # If it looks like a full task ID, return as-is
    if task_ref.startswith("task_"):
        return task_ref
    
    # Try to resolve as alias
    cache = load_cache(cache_path)
    resolved = cache.get("aliases", {}).get(task_ref)
    
    if resolved:
        return resolved
    
    # Not found - return original (let the API fail with proper error)
    return task_ref


def get_alias(task_id: str, cache_path: Path = CACHE_FILE) -> Optional[str]:
    """Get the alias for a task ID, if any."""
    cache = load_cache(cache_path)
    return cache.get("reverse", {}).get(task_id)


def format_task_with_alias(task: dict, cache_path: Path = CACHE_FILE) -> dict:
    """Add alias info to a task dict for display."""
    task_id = task.get("id", "")
    alias = get_alias(task_id, cache_path)
    if alias:
        task["_alias"] = alias
    return task
