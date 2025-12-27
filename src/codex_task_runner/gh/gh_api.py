from __future__ import annotations

"""Compatibility re-export for GitHub helpers.

This module gathers the public helpers from the split implementations
(`gh_api_cli` and `gh_api_graphql`) so existing imports continue to work.
"""

from .gh_api_cli import (
    pr_exists_open,
    create_pr,
    merge_pr,
    list_branches,
)
from .gh_api_graphql import (
    get_pr,
)

__all__ = [
    "pr_exists_open",
    "create_pr",
    "get_pr",
    "merge_pr",
    "list_branches",
]
