"""Merge a single task's PR."""
from ..gh.get_pr import get_pr
from ..gh.merge_pr import merge_pr


def merge_task(task, dry_run: bool = False) -> str:
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
