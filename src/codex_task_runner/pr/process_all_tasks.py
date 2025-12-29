"""Process all tasks: create PR, dedup, merge."""
from .process_task import process_task
from ..etc.log import log


def process_all_tasks(session, tasks: list, repo_filter: str | None, limit: int, 
                     dry_run: bool = False, create_followup: bool = False) -> dict:
    """Process each task and return totals."""
    totals = {"created": 0, "merged": 0, "skipped": 0, "failed": 0, "followup_created": 0}
    
    for i, task in enumerate(tasks, 1):
        log.info(f"\n[{i}/{len(tasks)}] {task.title[:60]}")
        result = process_task(session, task, repo_filter, limit, dry_run=dry_run, 
                            create_followup=create_followup)
        for k in totals:
            totals[k] += result.get(k, 0)
    
    if dry_run:
        totals["dry_run"] = True
    return totals
