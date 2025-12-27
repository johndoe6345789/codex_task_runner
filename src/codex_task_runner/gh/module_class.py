from __future__ import annotations

from codex_task_runner.gh.pr_exists_open import pr_exists_open
from codex_task_runner.gh.create_pr import create_pr, _parse_created_number
from codex_task_runner.gh.merge_pr import merge_pr
from codex_task_runner.gh.list_branches import list_branches
from codex_task_runner.gh.get_pr import get_pr, _parse_pr, _checks_state, _PR_QUERY
from codex_task_runner.gh.gh_api_call import gh_api
from codex_task_runner.gh.gh_graphql import gh_graphql
from codex_task_runner.gh.gh_vars import gh_vars


class GhModule:
    """Aggregates GitHub helpers across the `gh` package."""

    # CLI helpers
    pr_exists_open = staticmethod(pr_exists_open)
    create_pr = staticmethod(create_pr)
    _parse_created_number = staticmethod(_parse_created_number)
    merge_pr = staticmethod(merge_pr)
    list_branches = staticmethod(list_branches)

    # GraphQL helpers
    _pr_graphql_query = _PR_QUERY
    get_pr = staticmethod(get_pr)
    _parse_pr = staticmethod(_parse_pr)
    _checks_state = staticmethod(_checks_state)

    # low-level helpers
    _api = staticmethod(gh_api)
    _graphql = staticmethod(gh_graphql)
    _vars = staticmethod(gh_vars)
