"""Extract git patch from a Codex task."""
from typing import Any
import sys


def get_patch_from_task(session, task_id: str, turn_id: str | None = None) -> dict:
    """Extract the git diff patch from a task's turn output."""
    # Get turns for the task
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns"
    resp = session.get(url)
    
    if not resp.ok:
        return {"error": f"Failed to get turns: {resp.status_code}", "text": resp.text}
    
    turns_data = resp.json()
    
    # Use provided turn_id or current turn
    if not turn_id:
        turn_id = turns_data.get("current_turn_id")
    
    if not turn_id:
        return {"error": "No turn_id found"}
    
    # Get the turn from mapping
    turn_mapping = turns_data.get("turn_mapping", {})
    if turn_id not in turn_mapping:
        return {"error": f"Turn {turn_id} not found in mapping"}
    
    turn = turn_mapping[turn_id].get("turn", {})
    output_items = turn.get("output_items", [])
    
    # Find the PR item with output_diff
    for item in output_items:
        if item.get("type") == "pr" and "output_diff" in item:
            output_diff = item["output_diff"]
            diff = output_diff.get("diff", "")
            return {
                "task_id": task_id,
                "turn_id": turn_id,
                "pr_title": item.get("pr_title", ""),
                "pr_message": item.get("pr_message", ""),
                "repo_id": output_diff.get("repo_id", ""),
                "base_commit_sha": output_diff.get("base_commit_sha", ""),
                "diff": diff,
                "diff_lines": len(diff.split("\n")) if diff else 0,
            }
    
    return {"error": "No diff found in task output_items", "output_item_types": [i.get("type") for i in output_items]}


def handle(args: Any, session) -> dict | str:
    """Extract git patch from a task."""
    task_id = args.task_id
    turn_id = getattr(args, "turn_id", None)
    raw = getattr(args, "raw", False)
    output_file = getattr(args, "output", None)
    
    result = get_patch_from_task(session, task_id, turn_id)
    
    if "error" in result:
        return result
    
    diff = result.get("diff", "")
    
    # Write to file if requested
    if output_file:
        with open(output_file, "w") as f:
            f.write(diff)
        result["saved_to"] = output_file
    
    # Return raw diff if requested (for piping to git apply)
    if raw:
        print(diff, end="")
        sys.exit(0)
    
    return result
