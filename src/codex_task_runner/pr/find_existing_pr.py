"""Find existing open PR for a task."""
from ..proc.run import run
from ..etc.log import log
from ..etc.slugify import slugify
import json
import re


def _normalize(s: str) -> str:
    """Normalize title for comparison: lowercase, strip punctuation/whitespace."""
    s = s.lower()
    s = re.sub(r'[^\w\s]', '', s)  # remove punctuation
    s = re.sub(r'\s+', ' ', s).strip()  # collapse whitespace
    return s


def _titles_match(a: str, b: str) -> bool:
    """Check if titles match (normalized or one contains the other)."""
    na, nb = _normalize(a), _normalize(b)
    if na == nb:
        return True
    # Check if one contains the other (for truncated titles)
    if na in nb or nb in na:
        return True
    return False


def find_existing_pr(repo: str, title: str) -> int | None:
    """Check if an open PR with this title or matching branch already exists.
    
    Searches for PRs by:
    1. Matching title (normalized)
    2. Matching branch name (codex/slugified-title)
    
    Returns PR number if found, None otherwise.
    """
    # Search for open PRs with matching title or branch
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--state", "open",
        "--json", "number,title,headRefName",
        "--limit", "100",
    ]
    
    result = run(cmd)
    if result.code != 0:
        log.debug(f"gh pr list failed: {result.err}")
        return None
    
    try:
        prs = json.loads(result.out)
    except json.JSONDecodeError:
        return None
    
    # Generate expected branch name from title
    expected_branch = f"codex/{slugify(title)}"
    log.debug(f"Looking for PR with title '{title}' or branch '{expected_branch}'")
    
    # Find PR with matching title (normalized) or branch name
    for pr in prs:
        pr_title = pr.get("title", "")
        pr_branch = pr.get("headRefName", "")
        
        # Check title match
        if _titles_match(title, pr_title):
            log.debug(f"Title match: '{title}' ~ '{pr_title}'")
            return pr.get("number")
        
        # Check branch match (exact or with random suffix)
        if pr_branch == expected_branch:
            log.debug(f"Branch exact match: '{expected_branch}' = '{pr_branch}'")
            return pr.get("number")
        
        # Check if branch starts with expected (handles random suffixes)
        if pr_branch.startswith(expected_branch + "-"):
            log.debug(f"Branch prefix match: '{expected_branch}' ~ '{pr_branch}'")
            return pr.get("number")
    
    log.debug(f"No PR found for title '{title}' or branch '{expected_branch}'")
    return None
