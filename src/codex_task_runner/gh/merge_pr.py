from __future__ import annotations

from typing import Any

from codex_task_runner.proc.run import run
from codex_task_runner.etc.log import log


def merge_pr(repo: str, number: int, method: Any, delete_branch: bool,
             admin: bool, auto: bool, dry_run: bool) -> tuple[bool, str]:
    """Merge a PR. Returns (success, error_message)."""
    if dry_run:
        return True, ""
    cmd = ["gh", "pr", "merge", str(number), "--repo", repo,
           f"--{method.value}"]
    cmd += ["--delete-branch"] if delete_branch else []
    cmd += ["--admin"] if admin else []
    cmd += ["--auto"] if auto else []
    r = run(cmd)
    
    if r.code != 0:
        # Extract meaningful error from stderr
        error_msg = r.err.strip() if r.err else r.out.strip()
        if not error_msg:
            error_msg = f"gh pr merge returned exit code {r.code}"
        return False, error_msg
    
    return True, ""
