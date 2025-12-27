from typing import Any

from .dedup_prs import handle as dedup_handle
from ..pr.ensure_prs import ensure_prs
from ..codex.codex_tasks_list import get_tasks_list
from ..gh.get_pr import get_pr
from ..gh.merge_pr import merge_pr
from ..etc.log import log


def _merge_task(task, dry_run: bool) -> str:
    """Merge a single task's PR. Returns status string."""
    if not task.pr_numbers:
        return "SKIP: no PR"
    
    pr_num = task.pr_numbers[0]
    try:
        pr = get_pr(task.repo, pr_num)
    except Exception as e:
        return f"SKIP: can't fetch PR #{pr_num}: {e}"
    
    if pr.state != "open":
        return f"SKIP: PR #{pr_num} is {pr.state}"
    
    if not pr.mergeable:
        return f"SKIP: PR #{pr_num} not mergeable"
    
    if dry_run:
        return f"DRY RUN: would merge PR #{pr_num}"
    
    ok = merge_pr(
        task.repo, pr_num,
        method="squash",
        delete_branch=True,
        admin=True,
        auto=True,
        dry_run=False,
    )
    return f"MERGED PR #{pr_num}" if ok else f"FAIL: PR #{pr_num}"


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
    
    # Confirm before proceeding
    if not no_confirm and not dry_run:
        try:
            response = input(f"Proceed with {len(tasks)} tasks? [y/N] ")
            if response.lower() != 'y':
                log.info("Aborted")
                return {"aborted": True}
        except (EOFError, KeyboardInterrupt):
            log.info("Aborted")
            return {"aborted": True}
    
    # Process each task: create PR if needed, dedup, merge immediately
    results = {"created": 0, "merged": 0, "skipped": 0, "failed": 0}
    
    for i, task in enumerate(tasks, 1):
        log.info(f"\n[{i}/{len(tasks)}] {task.title[:60]}")
        
        # Step 1: Create PR if needed
        if not task.pr_numbers:
            log.info("  Creating PR...")
            pr_result = ensure_prs(session, [task])
            if pr_result["created"] > 0:
                results["created"] += 1
                log.info("  PR created")
                
                # Dedup immediately after creating
                log.info("  Deduplicating...")
                import argparse
                dedup_args = argparse.Namespace(repo=repo_filter, dry_run=dry_run)
                dedup_handle(dedup_args)
                
                # Refresh task to get PR number - refetch from API
                refreshed = get_tasks_list(session, limit=limit)
                for rt in refreshed:
                    if rt.task_id == task.task_id:
                        task = rt
                        break
            else:
                log.warning("  Failed to create PR")
                results["failed"] += 1
                continue
        
        # Step 2: Merge the PR
        log.info(f"  Merging PR #{task.pr_numbers[0] if task.pr_numbers else '?'}...")
        status = _merge_task(task, dry_run)
        log.info(f"  {status}")
        
        if "MERGED" in status:
            results["merged"] += 1
        elif "DRY RUN" in status:
            results["skipped"] += 1
        elif "SKIP" in status:
            results["skipped"] += 1
        else:
            results["failed"] += 1
    
    log.info(f"\nDone: {results}")
    return results

