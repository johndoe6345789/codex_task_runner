"""Process merge with interactive conflict handling."""
from typing import Optional, Tuple
from ..gh.get_pr import get_pr
from ..pr.merge_task import merge_task
from ..pr.create_followup_task import create_followup_task
from ..etc.conflict_menu import show_conflict_menu, show_conflict_actions
from ..etc.log import log


def merge_with_menu(session, task, pr_num: int, interactive: bool = True, 
                   auto_followup: bool = False, dry_run: bool = False) -> Tuple[str, Optional[dict]]:
    """
    Attempt to merge a PR with interactive conflict handling.
    
    Args:
        session: Authenticated session
        task: Task to merge
        pr_num: PR number
        interactive: If True, show menu on conflicts
        auto_followup: If True, automatically create follow-ups without menu
        dry_run: If True, don't make actual changes
    
    Returns:
        Tuple of (status_string, optional_followup_task)
    """
    # Try to merge
    status = merge_task(task, dry_run=dry_run)
    
    # If successful or dry-run, return immediately
    if "MERGED" in status or "DRY RUN" in status:
        return status, None
    
    # Check if this is a conflict/blocker we should handle
    is_actionable_conflict = any(keyword in status for keyword in [
        "merge conflicts",
        "CI checks",
        "not ready",
        "not mergeable",
        "FAIL:"
    ])
    
    if not is_actionable_conflict:
        return status, None
    
    # Extract reason from status
    if ":" in status:
        parts = status.split(":", 1)
        reason = parts[1].strip() if len(parts) > 1 else status
    else:
        reason = status
    
    # Auto-create follow-up if requested
    if auto_followup:
        log.info(f"  Auto-creating follow-up task...")
        followup = create_followup_task(session, task, pr_num, reason, auto_create=True)
        return status, followup
    
    # Interactive menu (if enabled and not in batch mode)
    if not interactive:
        return status, None
    
    # Fetch PR details for menu
    try:
        pr = get_pr(task.repo, pr_num)
        pr_url = pr.url
    except Exception:
        pr_url = f"https://github.com/{task.repo}/pull/{pr_num}"
    
    # Show the menu
    choice = show_conflict_menu(task, pr_num, reason)
    
    if choice == "followup":
        log.info(f"  Creating follow-up task...")
        followup = create_followup_task(session, task, pr_num, reason, auto_create=True)
        return status, followup
        
    elif choice == "skip":
        log.info(f"  Skipping PR #{pr_num}")
        return status, None
        
    elif choice == "view":
        show_conflict_actions(pr_url, reason)
        # Ask again what to do
        return merge_with_menu(session, task, pr_num, interactive, auto_followup, dry_run)
        
    elif choice == "retry":
        log.info(f"  Retrying merge...")
        # Try merge again
        return merge_with_menu(session, task, pr_num, interactive, auto_followup, dry_run)
        
    elif choice == "abort":
        log.warning(f"  User aborted processing")
        return "ABORT: user requested abort", None
    
    # Fallback
    return status, None
