from __future__ import annotations

from typing import Any

from codex_task_runner.proc.run import run


def merge_pr(repo: str, number: int, method: Any, delete_branch: bool,
             admin: bool, auto: bool, dry_run: bool) -> bool:
    if dry_run:
        return True
    cmd = ["gh", "pr", "merge", str(number), "--repo", repo,
           f"--{method.value}"]
    cmd += ["--delete-branch"] if delete_branch else []
    cmd += ["--admin"] if admin else []
    cmd += ["--auto"] if auto else []
    r = run(cmd)
    return r.code == 0
