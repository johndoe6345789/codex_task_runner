"""Create follow-up tasks for non-mergeable PRs."""
from __future__ import annotations
from typing import Optional

from ..codex.codex_create_task import create_task, get_default_environment
from ..gh.get_pr import get_pr
from ..etc.log import log


def create_followup_task(
    session,
    task,
    pr_num: int,
    reason: str,
    auto_create: bool = False
) -> Optional[dict]:
    """
    Create a follow-up task to address why a PR isn't mergeable.
    
    Args:
        session: Authenticated session
        task: The original task
        pr_num: PR number that couldn't be merged
        reason: Why the PR couldn't be merged
        auto_create: If True, creates task automatically. If False, just returns the prompt.
    
    Returns:
        Created task response or None
    """
    try:
        pr = get_pr(task.repo, pr_num)
    except Exception as e:
        log.warning(f"  Could not fetch PR #{pr_num} for follow-up: {e}")
        return None
    
    # Generate prompt based on the failure reason
    prompt = _generate_followup_prompt(task.title, pr_num, pr.url, reason, pr)
    
    if not auto_create:
        log.info(f"  Suggested follow-up task prompt:")
        log.info(f"  '{prompt}'")
        return {"prompt": prompt, "pr_url": pr.url}
    
    # Auto-create the task
    log.info(f"  Creating follow-up task for PR #{pr_num}...")
    
    # Get environment (use same as original task if possible)
    env = get_default_environment(session)
    if not env:
        log.warning("  No environment found, cannot create follow-up task")
        return None
    
    env_id = env.get("id")
    if not env_id:
        log.warning("  No environment ID, cannot create follow-up task")
        return None
    
    # Create the follow-up task
    result = create_task(
        session=session,
        prompt=prompt,
        environment_id=env_id,
        branch=task.base_branch or "main",
        best_of_n=1,
        qa_mode=False,
    )
    
    if result:
        task_id = result.get("id", "unknown")
        log.info(f"  ✓ Created follow-up task: {task_id}")
        log.info(f"    Prompt: {prompt[:80]}...")
        return result
    else:
        log.warning(f"  Failed to create follow-up task")
        return None


def _generate_followup_prompt(
    original_title: str,
    pr_num: int,
    pr_url: str,
    reason: str,
    pr
) -> str:
    """Generate a prompt for the follow-up task based on the failure reason."""
    
    # Extract the actual issue
    if "merge conflicts" in reason.lower():
        return (
            f"Fix merge conflicts in PR #{pr_num} ({pr_url})\n\n"
            f"Original task: {original_title}\n\n"
            f"The PR has merge conflicts that need to be resolved. "
            f"Please resolve the conflicts and update the PR."
        )
    
    elif "ci checks" in reason.lower() or "status check" in reason.lower():
        return (
            f"Fix CI failures in PR #{pr_num} ({pr_url})\n\n"
            f"Original task: {original_title}\n\n"
            f"The PR has failing CI checks: {reason}\n"
            f"Please fix the test failures or other CI issues and update the PR."
        )
    
    elif "not mergeable" in reason.lower():
        return (
            f"Make PR #{pr_num} mergeable ({pr_url})\n\n"
            f"Original task: {original_title}\n\n"
            f"The PR cannot be merged due to: {reason}\n"
            f"Please address the issues preventing merge and update the PR."
        )
    
    else:
        # Generic follow-up
        return (
            f"Address issues preventing merge of PR #{pr_num} ({pr_url})\n\n"
            f"Original task: {original_title}\n\n"
            f"The PR could not be merged: {reason}\n"
            f"Please investigate and fix the issues preventing the PR from being merged."
        )
