"""Process a single task: create PR, merge, then dedup."""
import argparse

from .merge_with_menu import merge_with_menu
from .merge_task import merge_task
from .ensure_prs import ensure_prs
from .find_existing_pr import find_existing_pr
from .create_followup_task import create_followup_task
from ..handlers.dedup_prs import handle as dedup_handle
from ..codex.codex_tasks_list import get_tasks_list
from ..etc.log import log


def process_task(session, task, repo_filter: str, limit: int, dry_run: bool = False, 
                 create_followup: bool = False, interactive: bool = True) -> dict:
    """Process one task: create PR if needed, merge, then dedup.
    
    Args:
        session: Authenticated session
        task: Task to process
        repo_filter: Repository filter
        limit: Task fetch limit
        dry_run: If True, don't make changes
        create_followup: If True, create follow-up tasks for non-mergeable PRs
        interactive: If True, show menu for conflicts; if False, auto-create follow-ups
    
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
            log.info("  [DRY RUN] Would merge PR")
            log.info("  [DRY RUN] Would dedup")
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
            if pr_num:
                log.info(f"  Got PR #{pr_num} from API response")
            
            # If we didn't get PR number from API, search for it by title/branch
            if not pr_num:
                log.info("  Searching for PR by title/branch...")
                try:
                    pr_num = find_existing_pr(task.repo, task.title)
                    if pr_num:
                        log.info(f"  Found PR #{pr_num}")
                    else:
                        log.warning(f"  Could not find PR with title: {task.title[:60]}...")
                except Exception as e:
                    log.warning(f"  PR search failed: {e}")
                
                # If still not found, try refreshing task list as last resort
                if not pr_num:
                    log.info("  Refreshing task list...")
                    try:
                        refreshed = get_tasks_list(session, limit=limit)
                        for rt in refreshed:
                            if rt.task_id == task.task_id:
                                task = rt
                                break
                        pr_num = task.pr_numbers[0] if task.pr_numbers else None
                        if pr_num:
                            log.info(f"  Found PR #{pr_num} from refreshed task list")
                        else:
                            log.warning(f"  Task {task.task_id} has no PR numbers after refresh")
                    except Exception as e:
                        log.warning(f"  Task list refresh failed: {e}")
        else:
            log.warning("  Failed to create PR")
            result["failed"] = 1
            return result
    
    # Step 3: Merge the PR
    if dry_run:
        log.info(f"  [DRY RUN] Would merge PR #{pr_num}")
        result["merged"] = 1
        return result
    
    if not pr_num:
        log.warning("  Could not find PR number after creation")
        log.warning(f"  Possible causes: API delay, PR creation failed, or title mismatch")
        log.warning(f"  Task: {task.task_id}")
        log.warning(f"  Expected title: {task.title[:80]}...")
        log.info("  SKIP: no PR")
        result["skipped"] = 1
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
    
    # Use interactive menu or fallback to direct merge
    if interactive:
        # Use interactive menu workflow
        status, followup = merge_with_menu(session, task, pr_num, 
                                           interactive=True, 
                                           auto_followup=False, 
                                           dry_run=False)
        log.info(f"  {status}")
        
        if followup:
            result["followup_created"] = True
        
        if "MERGED" in status:
            result["merged"] = 1
        elif "SKIP" in status or "ABORT" in status:
            result["skipped"] = 1
        else:
            result["failed"] = 1
    else:
        # Non-interactive: use direct merge with optional follow-up creation
        status = merge_task(task, dry_run=False)
        log.info(f"  {status}")
        
        if "MERGED" in status:
            result["merged"] = 1
        elif "SKIP" in status:
            result["skipped"] = 1
            
            # If enabled, create follow-up task for non-mergeable PRs
            if create_followup and not dry_run:
                # Extract the reason from status message
                reason = status.split(":", 1)[1].strip() if ":" in status else "not mergeable"
                
                # Don't create follow-ups for closed PRs or missing PRs
                if "is closed" not in reason and "is merged" not in reason and "no PR" not in reason:
                    log.info(f"  Creating follow-up task to address: {reason}")
                    followup = create_followup_task(session, task, pr_num, reason, auto_create=True)
                    if followup:
                        result["followup_created"] = True
        else:
            result["failed"] = 1
            
            # Also consider creating follow-up for hard failures
            if create_followup and not dry_run and "FAIL" in status:
                reason = status.split("-", 1)[1].strip() if "-" in status else "merge failed"
                log.info(f"  Creating follow-up task to address: {reason}")
                followup = create_followup_task(session, task, pr_num, reason, auto_create=True)
                if followup:
                    result["followup_created"] = True
    
    # Step 4: Dedup after merge (cleanup duplicates)
    if not dry_run and result["merged"] == 1:
        log.info("  Deduplicating...")
        dedup_args = argparse.Namespace(repo=repo_filter, dry_run=False)
        dedup_handle(dedup_args)
    
    return result
    
    