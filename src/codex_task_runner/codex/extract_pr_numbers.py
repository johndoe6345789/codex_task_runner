from __future__ import annotations

from typing import Any


def extract_pr_numbers(pull_requests: Any) -> list[int]:
    if not isinstance(pull_requests, list):
        return []
    nums: list[int] = []
    for prwrap in pull_requests:
        n = _extract_one(prwrap)
        if n is not None:
            nums.append(n)
    return nums


def _extract_one(prwrap: Any) -> int | None:
    if not isinstance(prwrap, dict):
        return None
    pr = prwrap.get("pull_request")
    if not isinstance(pr, dict):
        return None
    n = pr.get("number")
    return int(n) if isinstance(n, int) else None
