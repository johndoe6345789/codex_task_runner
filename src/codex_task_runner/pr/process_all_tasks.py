"""Process all tasks: create PR, dedup, merge."""
from .process_task import process_task
from ..etc.blocklist import is_blocked
from ..etc.log import log


def process_all_tasks(session, tasks: list, repo_filter: str | None, limit: int, 
                     dry_run: bool = False, create_followup: bool = False, 
                     interactive: bool = True) -> dict:
    """Process each task and return totals.
    
    Args:
        session: Authenticated session
        tasks: List of tasks to process
        repo_filter: Repository filter
        limit: Task fetch limit
        dry_run: If True, don't make changes
        create_followup: If True, create follow-up tasks for non-mergeable PRs (non-interactive only)
        interactive: If True, show conflict menu; if False, auto-handle with create_followup flag
    """
    totals = {"created": 0, "merged": 0, "skipped": 0, "failed": 0, "followup_created": 0}
    
    for i, task in enumerate(tasks, 1):
        log.info(f"\n[{i}/{len(tasks)}] {task.title[:60]}")
        
        # Check if task is blocklisted
        if is_blocked(task.task_id):
            log.info(f"  SKIP: task {task.task_id} is in blocklist")
            totals["skipped"] += 1
            continue
        
        result = process_task(session, task, repo_filter, limit, dry_run=dry_run, 
                            create_followup=create_followup, interactive=interactive)
        for k in totals:
            totals[k] += result.get(k, 0)
    
    if dry_run:
        totals["dry_run"] = True
    return totals
