import json

from codex_task_runner.handlers import ping


def ping_cmd(sess, url: str) -> int:
    """Ping a single URL and print result."""
    from types import SimpleNamespace
    args = SimpleNamespace(url=url)
    res = ping.handle(args, sess)
    print(json.dumps(res, indent=2))
    return 0
