from __future__ import annotations

from ..types import PullRequest


def fmt_pr(pr: PullRequest) -> str:
    return (
        f"PR #{pr.number}: {pr.title}\n"
        f"  url={pr.url}\n"
        f"  author={pr.author} mergeable={pr.mergeable} checks={pr.checks_state}\n"
    )
