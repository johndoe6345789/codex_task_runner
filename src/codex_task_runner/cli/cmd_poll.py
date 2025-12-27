from codex_task_runner.handlers import poll


def poll_cmd(sess, urls_file: str, out: str) -> int:
    """Poll a list of URLs from a file and save JSON."""
    from types import SimpleNamespace
    args = SimpleNamespace(urls_file=urls_file, out=out)
    res = poll.handle(args, sess)
    print(f"saved results to {res.get('saved', out)}")
    return 0
