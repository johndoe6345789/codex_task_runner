"""Create a new Codex task via the API."""
from __future__ import annotations

from typing import Optional

from ..etc.log import log
from .json_post import _json_post


def create_task(
    session,
    prompt: str,
    environment_id: str,
    branch: str = "main",
    best_of_n: int = 1,
    qa_mode: bool = False,
) -> Optional[dict]:
    """
    Create a new Codex task.
    
    Args:
        session: Authenticated requests session
        prompt: The task prompt/description
        environment_id: The Codex environment ID (from /wham/environments)
        branch: Git branch to work on (default: "main")
        best_of_n: Number of parallel attempts (default: 1)
        qa_mode: Run in QA mode (default: False)
    
    Returns:
        Task creation response or None on failure
    """
    url = "https://chatgpt.com/backend-api/wham/tasks"
    
    payload = {
        "new_task": {
            "environment_id": environment_id,
            "branch": branch,
            "run_environment_in_qa_mode": qa_mode,
        },
        "metadata": {
            "best_of_n": best_of_n,
        },
        "input_items": [
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "content_type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
    }
    
    log.debug(f"Creating task with prompt: {prompt[:50]}...")
    return _json_post(session, url, payload)


def get_default_environment(session) -> Optional[dict]:
    """Get the most recently used environment."""
    from .json_get import _json_get
    
    url = "https://chatgpt.com/backend-api/wham/environments/recent"
    result = _json_get(session, url)
    
    if result and isinstance(result, list) and len(result) > 0:
        return result[0]
    
    # Fallback to listing all environments
    url = "https://chatgpt.com/backend-api/wham/environments"
    result = _json_get(session, url)
    
    if result and isinstance(result, list) and len(result) > 0:
        return result[0]
    
    return None
