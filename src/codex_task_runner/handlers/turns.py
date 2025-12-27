from typing import Any, Optional

from ..codex_cloud import get_turns


def handle(args: Any, session) -> Optional[dict]:
    return get_turns(session, args.task_id)
