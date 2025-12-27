"""Find and close duplicate PRs, keeping the newest one."""
from typing import Any
from collections import defaultdict
import subprocess
import json

from ..etc.log import log


def _get_open_prs(repo: str) -> list[dict]:
    """Get all open PRs for a repo."""
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", repo, "--state", "open", "--limit", "500",
         "--json", "number,headRefName,title,createdAt"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        log.error(f"Failed to list PRs: {result.stderr}")
        return []
    return json.loads(result.stdout)


def _close_pr(repo: str, pr_number: int, dry_run: bool) -> bool:
    """Close a PR."""
    if dry_run:
        log.info(f"  [DRY RUN] Would close PR #{pr_number}")
        return True
    
    result = subprocess.run(
        ["gh", "pr", "close", str(pr_number), "--repo", repo, "--delete-branch"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        log.error(f"  Failed to close PR #{pr_number}: {result.stderr}")
        return False
    log.info(f"  Closed PR #{pr_number}")
    return True


def _normalize_branch(branch: str) -> str:
    """Normalize branch name by removing random suffix."""
    # codex/foo-bar-baz-abc123 -> codex/foo-bar-baz
    # The suffix is typically 6 alphanumeric chars after final dash
    import re
    match = re.match(r'^(codex/.+)-[a-z0-9]{6}$', branch)
    if match:
        return match.group(1)
    return branch


def handle(args: Any, session=None) -> dict:
    """Find and close duplicate PRs."""
    repo = getattr(args, "repo", "johndoe6345789/metabuilder")
    dry_run = getattr(args, "dry_run", False)
    
    log.info(f"Fetching open PRs for {repo}...")
    prs = _get_open_prs(repo)
    log.info(f"Found {len(prs)} open PRs")
    
    # Group by normalized branch name (title is more reliable actually)
    by_title = defaultdict(list)
    for pr in prs:
        by_title[pr["title"]].append(pr)
    
    # Find duplicates
    duplicates = {title: prs for title, prs in by_title.items() if len(prs) > 1}
    
    if not duplicates:
        log.info("No duplicate PRs found")
        return {"duplicates": 0}
    
    log.info(f"Found {len(duplicates)} sets of duplicate PRs:")
    
    closed = 0
    kept = 0
    for title, dup_prs in duplicates.items():
        # Sort by PR number (highest = newest)
        dup_prs.sort(key=lambda p: p["number"], reverse=True)
        
        keep = dup_prs[0]
        to_close = dup_prs[1:]
        
        log.info(f"\n'{title[:60]}...'")
        log.info(f"  Keep: PR #{keep['number']} ({keep['headRefName']})")
        
        for pr in to_close:
            if _close_pr(repo, pr["number"], dry_run):
                closed += 1
        kept += 1
    
    log.info(f"\nSummary: Kept {kept} PRs, closed {closed} duplicates")
    return {"kept": kept, "closed": closed, "dry_run": dry_run}
