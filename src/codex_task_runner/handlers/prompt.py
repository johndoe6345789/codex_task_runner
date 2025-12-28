"""Handler for creating a new Codex task (send prompt)."""
from typing import Any

from ..codex.codex_create_task import create_task, get_default_environment
from ..codex.json_get import _json_get


def handle(args: Any, session) -> dict:
    """
    Create a new Codex task with the given prompt.
    
    Requires:
        - prompt: The task description
        
    Optional:
        - --env-id: Specific environment ID (default: most recent)
        - --branch: Git branch (default: main)
        - --best-of: Number of parallel attempts (default: 1)
    """
    prompt = getattr(args, "prompt", None)
    if not prompt:
        return {"error": "No prompt provided"}
    
    # Get environment ID
    env_id = getattr(args, "env_id", None)
    if not env_id:
        # Try to get the default/recent environment
        env = get_default_environment(session)
        if env:
            env_id = env.get("id") or env.get("environment_id")
            env_name = env.get("name") or env.get("full_name") or "unknown"
            print(f"Using environment: {env_name} ({env_id})")
        else:
            return {"error": "No environment found. Please specify --env-id or connect a repository in Codex."}
    
    branch = getattr(args, "branch", "main")
    best_of_n = getattr(args, "best_of", 1)
    
    # Create the task
    result = create_task(
        session=session,
        prompt=prompt,
        environment_id=env_id,
        branch=branch,
        best_of_n=best_of_n,
    )
    
    if result is None:
        return {"error": "Failed to create task. Check your authentication."}
    
    # Extract useful info from result
    task_id = result.get("task_id") or result.get("id")
    
    return {
        "success": True,
        "task_id": task_id,
        "prompt": prompt[:100] + ("..." if len(prompt) > 100 else ""),
        "branch": branch,
        "environment_id": env_id,
        "raw_response": result,
    }
