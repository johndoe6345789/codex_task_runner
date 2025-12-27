from typing import Any

from .run import handle as run_handle
from ..pr.ensure_prs import ensure_prs
from ..codex.codex_tasks_list import get_tasks_list
from ..etc.log import log


def handle(args: Any, session) -> dict:
    """YOLO mode: create PRs via Codex, then merge all tasks."""
    from ..etc.set_level import set_level
    
    # Enable debug logging if verbose
    if getattr(args, "verbose", False):
        set_level("DEBUG")
    
    # First, get tasks and create PRs for those without
    log.info("Fetching tasks...")
    tasks = get_tasks_list(session, limit=20)
    if not tasks:
        log.error("No tasks found")
        return {"processed": 0, "error": "no tasks"}
    
    log.info(f"Found {len(tasks)} tasks")
    pr_result = ensure_prs(session, tasks)
    log.info(f"PRs: {pr_result['created']} created, {pr_result['skipped']} already had PR")
    if pr_result['errors']:
        log.warning(f"Errors: {pr_result['errors']}")
    
    # Now run the merge process
    log.info("Starting merge process...")
    args.yolo = True
    args.dry_run = False
    result = run_handle(args, session)
    result["prs_created"] = pr_result["created"]
    log.info(f"Done: {result}")
    return result

