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
    
    # Get limit (default 5 for safety)
    limit = getattr(args, "limit", 5) or 5
    repo_filter = getattr(args, "repo", None)
    no_confirm = getattr(args, "no_confirm", False)
    dry_run = getattr(args, "dry_run", False)
    
    # First, get tasks
    log.info(f"Fetching up to {limit} tasks...")
    tasks = get_tasks_list(session, limit=limit)
    if not tasks:
        log.error("No tasks found")
        return {"processed": 0, "error": "no tasks"}
    
    # Filter by repo if specified
    if repo_filter:
        tasks = [t for t in tasks if t.repo == repo_filter]
        log.info(f"Filtered to {len(tasks)} tasks for repo {repo_filter}")
    else:
        log.info(f"Found {len(tasks)} tasks")
    
    if not tasks:
        log.warning("No tasks match filter")
        return {"processed": 0, "filtered": True}
    
    # Show what we're about to do
    log.info("")
    log.info("Tasks to process:")
    for t in tasks:
        pr_status = f"PR #{t.pr_numbers[0]}" if t.pr_numbers else "no PR"
        log.info(f"  - {t.repo}: {t.title[:50]} ({pr_status})")
    log.info("")
    
    # Dry run - just show plan
    if dry_run:
        needs_pr = [t for t in tasks if not t.pr_numbers]
        has_pr = [t for t in tasks if t.pr_numbers]
        log.info(f"DRY RUN: Would create {len(needs_pr)} PRs, merge {len(has_pr)} existing")
        return {"dry_run": True, "would_create": len(needs_pr), "would_merge": len(has_pr)}
    
    # Confirm before proceeding
    if not no_confirm:
        try:
            response = input(f"Proceed with {len(tasks)} tasks? [y/N] ")
            if response.lower() != 'y':
                log.info("Aborted")
                return {"aborted": True}
        except (EOFError, KeyboardInterrupt):
            log.info("Aborted")
            return {"aborted": True}
    
    # Create PRs for tasks without them
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

