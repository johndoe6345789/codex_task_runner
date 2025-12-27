import json

from codex_task_runner.handlers import turns


def turns_cmd(sess, task_id: str) -> int:
    """Fetch turns for a task."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id)
    data = turns.handle(args, sess)
    print(json.dumps(data or {}, indent=2))
    return 0
