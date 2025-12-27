from __future__ import annotations

from codex_task_runner.types import PullRequest


def is_clean(pr: PullRequest, require_checks: bool) -> bool:
    if pr.mergeable != "MERGEABLE":
        return False
    if not require_checks:
        return True
    return pr.checks_state == "SUCCESS"
