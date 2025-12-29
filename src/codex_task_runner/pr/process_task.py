"""Process a single task: create PR, dedup, merge."""
import argparse

from .merge_task import merge_task
from .ensure_prs import ensure_prs
from .find_existing_pr import find_existing_pr
from ..handlers.dedup_prs import handle as dedup_handle
from ..codex.codex_tasks_list import get_tasks_list
from ..etc.log import log


def process_task(session, task, repo_filter: str, limit: int, dry_run: bool = False) -> dict:
    """Process one task: create PR if needed, dedup, merge.
    
    Returns dict with keys: created, merged, skipped, failed (each 0 or 1)
    """
    result = {"created": 0, "merged": 0, "skipped": 0, "failed": 0}
    
    # Step 1: Check if PR already exists (either in task or on GitHub)
    pr_num = None
    if task.pr_numbers:
        pr_num = task.pr_numbers[0]
    else:
        # Check GitHub for existing open PR with same title
        existing = find_existing_pr(task.repo, task.title)
        if existing:
            log.info(f"  Found existing PR #{existing}")
            pr_num = existing
    
    # Step 2: Create PR if still needed
    if not pr_num:
        if dry_run:
            log.info("  [DRY RUN] Would create PR")
            log.info("  [DRY RUN] Would dedup")
            log.info("  [DRY RUN] Would merge PR")
            result["created"] = 1
            result["merged"] = 1
            return result
        
        log.info("  Creating PR...")
        pr_result = ensure_prs(session, [task])
        if pr_result["created"] > 0:
            result["created"] = 1
            log.info("  PR created")
            
            # Get PR number from the result
            pr_num = pr_result.get("pr_numbers", {}).get(task.task_id)
            
            # Dedup immediately after creating
            log.info("  Deduplicating...")
            dedup_args = argparse.Namespace(repo=repo_filter, dry_run=False)
            dedup_handle(dedup_args)
            
            # If we didn't get PR number from API, try refreshing task list as fallback
            if not pr_num:
                log.debug("  PR number not in API response, refreshing task list...")
                refreshed = get_tasks_list(session, limit=limit)
                for rt in refreshed:
                    if rt.task_id == task.task_id:
                        task = rt
                        break
                pr_num = task.pr_numbers[0] if task.pr_numbers else None
        else:
            log.warning("  Failed to create PR")
            result["failed"] = 1
            return result
    
    # Step 3: Merge the PR
    if dry_run:
        log.info(f"  [DRY RUN] Would merge PR #{pr_num}")
        result["merged"] = 1
        return result
    
    log.info(f"  Merging PR #{pr_num}...")
    # Update task with found PR number if we found one on GitHub
    if pr_num and not task.pr_numbers:
        # Create a modified task with the found PR
        from ..etc.task_ref import TaskRef
        task = TaskRef(
            task_id=task.task_id,
            title=task.title,
            repo=task.repo,
            base_branch=task.base_branch,
            pr_numbers=(pr_num,),
        )
    
    status = merge_task(task, dry_run=False)
    log.info(f"  {status}")
    
    if "MERGED" in status:
        result["merged"] = 1
    elif "SKIP" in status:
        result["skipped"] = 1
    else:
        result["failed"] = 1
    
    return result
