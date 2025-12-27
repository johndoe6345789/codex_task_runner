from __future__ import annotations

from typing import Optional

from .json_get import _json_get


def get_turns(session, task_id: str) -> Optional[dict]:
    url = f"https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns"
    return _json_get(session, url)
