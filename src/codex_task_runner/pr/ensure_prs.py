import re
from ..codex.codex_turns import get_turns
from ..codex.codex_create_pr import create_pr_for_turn
from ..etc.log import log


def _extract_pr_number_from_url(url: str) -> int | None:
    """Extract PR number from GitHub PR URL."""
    if not url:
        return None
    # Match patterns like:
    # https://github.com/owner/repo/pull/123
    # http://github.com/owner/repo/pull/123
    match = re.search(r'/pull/(\d+)', url)
    if match:
        return int(match.group(1))
    return None


def ensure_prs(session, tasks) -> dict:
    """Create PRs via Codex API for tasks that don't have one.
    
    Returns dict with keys:
    - created: number of PRs created
    - skipped: number of tasks skipped
    - errors: list of error messages
    - pr_numbers: dict mapping task_id to PR number for newly created PRs
    """
    created = 0
    skipped = 0
    errors = []
    pr_numbers = {}  # task_id -> pr_number
    
    for t in tasks:
        if t.pr_numbers:
            log.debug(f"SKIP {t.task_id}: already has PR {t.pr_numbers}")
            skipped += 1
            continue
        
        # Get turns for this task
        log.info(f"GET turns for {t.task_id}: {t.title[:40]}")
        turns_data = get_turns(session, t.task_id)
        if not turns_data:
            log.warning(f"FAIL {t.task_id}: no turns data")
            errors.append(f"{t.task_id}: no turns")
            continue
        
        # The API returns turn_mapping and current_turn_id
        # Use current_turn_id directly as the last turn
        current_turn_id = turns_data.get("current_turn_id")
        if current_turn_id:
            turn_id = current_turn_id
            log.debug(f"Using current_turn_id: {turn_id}")
        else:
            # Fallback: try to extract from turn_mapping
            turn_mapping = turns_data.get("turn_mapping") or {}
            if not turn_mapping:
                log.warning(f"FAIL {t.task_id}: no turn_mapping")
                errors.append(f"{t.task_id}: no turns")
                continue
            
            # Get the last key from turn_mapping
            turn_ids = list(turn_mapping.keys())
            if not turn_ids:
                log.warning(f"FAIL {t.task_id}: empty turn_mapping")
                errors.append(f"{t.task_id}: empty turns")
                continue
            
            turn_id = turn_ids[-1]
            log.debug(f"Using last turn from mapping: {turn_id}")
        
        # Create PR via Codex API
        log.info(f"CREATE PR for {t.task_id} turn {turn_id}")
        result = create_pr_for_turn(session, t.task_id, str(turn_id))
        if result:
            created += 1
            # Extract PR number from the response
            pr_url = result.get("pr_url") or result.get("url") or ""
            pr_num = _extract_pr_number_from_url(pr_url)
            if pr_num:
                pr_numbers[t.task_id] = pr_num
                log.info(f"OK {t.task_id}: PR #{pr_num} created")
            else:
                if pr_url:
                    log.info(f"OK {t.task_id}: PR created but could not extract number from URL: {pr_url}")
                else:
                    log.info(f"OK {t.task_id}: PR created (no URL in API response)")
        else:
            log.error(f"FAIL {t.task_id}: API returned None")
            errors.append(f"{t.task_id}: API failed")
    
    return {
        "created": created,
        "skipped": skipped,
        "errors": errors,
        "pr_numbers": pr_numbers,
    }
