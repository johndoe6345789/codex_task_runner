"""Persistent blocklist for tasks that should be skipped."""
import json
from pathlib import Path
from typing import Set
from ..etc.log import log


def get_blocklist_path() -> Path:
    """Get path to blocklist file in user's home directory."""
    config_dir = Path.home() / ".config" / "codex-task-runner"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "blocklist.json"


def load_blocklist() -> Set[str]:
    """Load blocklist from disk.
    
    Returns:
        Set of blocked task IDs
    """
    blocklist_path = get_blocklist_path()
    if not blocklist_path.exists():
        return set()
    
    try:
        with open(blocklist_path, 'r') as f:
            data = json.load(f)
            return set(data.get("blocked_tasks", []))
    except Exception as e:
        log.warning(f"Failed to load blocklist: {e}")
        return set()


def save_blocklist(blocked_tasks: Set[str]) -> None:
    """Save blocklist to disk.
    
    Args:
        blocked_tasks: Set of task IDs to block
    """
    blocklist_path = get_blocklist_path()
    try:
        data = {"blocked_tasks": sorted(list(blocked_tasks))}
        with open(blocklist_path, 'w') as f:
            json.dump(data, f, indent=2)
        log.info(f"Blocklist saved to {blocklist_path}")
    except Exception as e:
        log.error(f"Failed to save blocklist: {e}")


def add_to_blocklist(task_id: str) -> bool:
    """Add a task ID to the blocklist.
    
    Args:
        task_id: Task ID to block
    
    Returns:
        True if added successfully
    """
    blocked = load_blocklist()
    if task_id in blocked:
        log.info(f"Task {task_id} is already in blocklist")
        return False
    
    blocked.add(task_id)
    save_blocklist(blocked)
    log.info(f"Added task {task_id} to blocklist")
    return True


def remove_from_blocklist(task_id: str) -> bool:
    """Remove a task ID from the blocklist.
    
    Args:
        task_id: Task ID to unblock
    
    Returns:
        True if removed successfully
    """
    blocked = load_blocklist()
    if task_id not in blocked:
        log.info(f"Task {task_id} is not in blocklist")
        return False
    
    blocked.remove(task_id)
    save_blocklist(blocked)
    log.info(f"Removed task {task_id} from blocklist")
    return True


def is_blocked(task_id: str) -> bool:
    """Check if a task is in the blocklist.
    
    Args:
        task_id: Task ID to check
    
    Returns:
        True if task is blocked
    """
    blocked = load_blocklist()
    return task_id in blocked


def clear_blocklist() -> int:
    """Clear all entries from the blocklist.
    
    Returns:
        Number of entries cleared
    """
    blocked = load_blocklist()
    count = len(blocked)
    save_blocklist(set())
    log.info(f"Cleared {count} entries from blocklist")
    return count


def list_blocklist() -> list:
    """Get list of all blocked task IDs.
    
    Returns:
        Sorted list of blocked task IDs
    """
    blocked = load_blocklist()
    return sorted(list(blocked))
