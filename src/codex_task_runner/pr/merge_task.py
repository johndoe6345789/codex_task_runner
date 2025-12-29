"""Merge a single task's PR."""
from ..gh.get_pr import get_pr
from ..gh.merge_pr import merge_pr
from ..etc.merge_method import MergeMethod


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
    
    # Provide detailed mergeable status
    if pr.mergeable == "CONFLICTING":
        return f"SKIP: PR #{pr_num} has merge conflicts"
    elif pr.mergeable == "UNKNOWN":
        return f"SKIP: PR #{pr_num} mergeable state unknown (GitHub still calculating)"
    elif not pr.mergeable or pr.mergeable != "MERGEABLE":
        reasons = []
        if pr.checks_state and pr.checks_state != "SUCCESS":
            reasons.append(f"CI checks: {pr.checks_state}")
        if not pr.mergeable:
            reasons.append("not mergeable")
        reason_str = ", ".join(reasons) if reasons else "unknown reason"
        return f"SKIP: PR #{pr_num} not ready ({reason_str})"
    
    if dry_run:
        return f"DRY RUN: would merge PR #{pr_num}"
    
    ok, error = merge_pr(
        task.repo, pr_num,
        method=MergeMethod.SQUASH,
        delete_branch=True,
        admin=True,
        auto=True,
        dry_run=False,
    )
    
    if ok:
        return f"MERGED PR #{pr_num}"
    else:
        # Include the actual error from gh CLI
        error_summary = error.split('\n')[0] if error else "merge failed"
        return f"FAIL: PR #{pr_num} - {error_summary}"
