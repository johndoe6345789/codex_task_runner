from __future__ import annotations

from codex_task_runner.gh.get_pr import get_pr


def _first_open(repo: str, nums: list[int]) -> int | None:
    for n in nums:
        try:
            pr = get_pr(repo, n)
        except Exception:
            continue
        if pr.mergeable:
            return n
    return None
