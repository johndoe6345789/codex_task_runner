import json

from codex_task_runner.handlers import create_pr


def create_pr_cmd(sess, task_id: str, turn_id: str, dry_run: bool) -> int:
    """Create PR for a task turn (calls Codex API)."""
    from types import SimpleNamespace
    args = SimpleNamespace(task_id=task_id, turn_id=turn_id, dry_run=dry_run)
    if dry_run:
        print("dry-run: not creating PR")
        return 0
    resp = create_pr.handle(args, sess)
    print(json.dumps(resp or {}, indent=2))
    return 0
