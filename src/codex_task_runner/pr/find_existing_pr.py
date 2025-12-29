"""Find existing open PR for a task."""
from ..proc.run import run
from ..etc.log import log
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
    """Check if an open PR with this title already exists.
    
    Returns PR number if found, None otherwise.
    """
    # Search for open PRs with matching title
    cmd = [
        "gh", "pr", "list",
        "--repo", repo,
        "--state", "open",
        "--json", "number,title",
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
    
    # Find PR with matching title (normalized)
    for pr in prs:
        pr_title = pr.get("title", "")
        if _titles_match(title, pr_title):
            log.debug(f"Title match: '{title}' ~ '{pr_title}'")
            return pr.get("number")
    
    return None
