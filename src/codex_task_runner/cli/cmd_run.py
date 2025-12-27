from typing import Optional

from codex_task_runner.handlers import run


def run_cmd(sess, dry_run: bool, output_dir: Optional[str]) -> int:
    """Run integration: fetch tasks and process."""
    from types import SimpleNamespace
    args = SimpleNamespace(dry_run=dry_run, output_dir=output_dir)
    res = run.handle(args, sess)
    processed = res.get("processed", 0)
    if res.get("error"):
        print("No tasks found or request failed.")
        return 1
    print(f"Processed {processed} tasks (dry-run={dry_run}).")
    return 0
