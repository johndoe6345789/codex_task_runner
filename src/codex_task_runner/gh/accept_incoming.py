"""Force merge PR by accepting incoming changes."""
import subprocess
from ..etc.log import log
from ..gh.get_pr import get_pr


def accept_incoming_changes(repo: str, pr_num: int, dry_run: bool = False) -> tuple[bool, str]:
    """
    Force merge PR by accepting incoming changes (theirs strategy).
    
    This checks out the PR branch locally, merges with strategy 'theirs',
    pushes the result, and then attempts to merge the PR on GitHub.
    
    Args:
        repo: Repository in format "owner/repo"
        pr_num: PR number
        dry_run: If True, only simulate
    
    Returns:
        Tuple of (success, message)
    """
    if dry_run:
        return True, f"DRY RUN: Would accept incoming changes for PR #{pr_num}"
    
    try:
        # Get PR details
        pr = get_pr(repo, pr_num)
        head_ref = pr.head_ref  # Branch name
        
        if not head_ref:
            return False, f"Could not determine head ref for PR #{pr_num}"
        
        log.info(f"  Fetching PR #{pr_num} branch: {head_ref}")
        
        # Fetch the PR branch
        result = subprocess.run(
            ["gh", "pr", "checkout", str(pr_num)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, f"Failed to checkout PR: {result.stderr}"
        
        log.info(f"  Merging with strategy 'theirs' (accept incoming)")
        
        # Merge with theirs strategy (accept all incoming changes)
        result = subprocess.run(
            ["git", "merge", "-X", "theirs", "origin/main"],  # Adjust base branch if needed
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            # Try to abort the merge if it failed
            subprocess.run(["git", "merge", "--abort"], capture_output=True)
            return False, f"Merge failed: {result.stderr}"
        
        log.info(f"  Pushing merged changes")
        
        # Push the merged changes
        result = subprocess.run(
            ["git", "push"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, f"Push failed: {result.stderr}"
        
        log.info(f"  Attempting to merge PR #{pr_num} on GitHub")
        
        # Now try to merge the PR on GitHub
        result = subprocess.run(
            ["gh", "pr", "merge", str(pr_num), "--auto", "--squash"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, f"MERGED PR #{pr_num} (with incoming changes accepted)"
        else:
            # PR might still merge after CI passes
            return True, f"Changes pushed for PR #{pr_num}, may auto-merge after CI"
        
    except Exception as e:
        log.error(f"Error accepting incoming changes: {e}")
        return False, f"Error: {str(e)}"
