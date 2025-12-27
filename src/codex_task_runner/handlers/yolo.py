"""YOLO mode: create PRs, dedup, merge - full automation."""
from typing import Any

from ..codex.codex_tasks_list import get_tasks_list
from ..pr.filter_tasks import filter_tasks
from ..pr.show_tasks import show_tasks
from ..pr.process_task import process_task
from ..etc.confirm import confirm
from ..etc.log import log


def handle(args: Any, session) -> dict:
    """YOLO mode: create PRs via Codex, then merge all tasks."""
    from ..etc.set_level import set_level
    
    if getattr(args, "verbose", False):
        set_level("DEBUG")
    
    limit = getattr(args, "limit", 5) or 5
    repo_filter = getattr(args, "repo", None)
    no_confirm = getattr(args, "no_confirm", False)
    dry_run = getattr(args, "dry_run", False)
    
    # Fetch and filter tasks
    log.info(f"Fetching up to {limit} tasks...")
    tasks = get_tasks_list(session, limit=limit)
    if not tasks:
        log.error("No tasks found")
        return {"processed": 0, "error": "no tasks"}
    
    tasks = filter_tasks(tasks, repo_filter)
    log.info(f"Found {len(tasks)} tasks" + (f" for {repo_filter}" if repo_filter else ""))
    
    if not tasks:
        log.warning("No tasks match filter")
        return {"processed": 0, "filtered": True}
    
    # Show plan
    needs_pr, has_pr = show_tasks(tasks)
    
    # Dry run exits early
    if dry_run:
        log.info(f"DRY RUN: Would create {len(needs_pr)} PRs, merge {len(tasks)} total")
        return {"dry_run": True, "would_create": len(needs_pr), "would_merge": len(has_pr)}
    
    # Confirm
    if not no_confirm and not confirm(f"Proceed with {len(tasks)} tasks?"):
        return {"aborted": True}
    
    # Process each task
    totals = {"created": 0, "merged": 0, "skipped": 0, "failed": 0}
    
    for i, task in enumerate(tasks, 1):
        log.info(f"\n[{i}/{len(tasks)}] {task.title[:60]}")
        result = process_task(session, task, repo_filter, limit)
        for k in totals:
            totals[k] += result.get(k, 0)
    
    log.info(f"\nDone: {totals}")
    return totals

