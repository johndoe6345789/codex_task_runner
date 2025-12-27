import json

from codex_task_runner.handlers import tasks


def tasks_cmd(sess, limit: int) -> int:
    """List tasks from Codex Cloud."""
    from types import SimpleNamespace
    args = SimpleNamespace(limit=limit)
    res = tasks.handle(args, sess)
    print(json.dumps(res, indent=2))
    return 0
