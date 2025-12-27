from __future__ import annotations

from typing import Optional

from .json_post import _json_post


def create_pr_for_turn(session, task_id: str, turn_id: str) -> Optional[dict]:
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns/{turn_id}/pr"
    return _json_post(session, url, data={})
