from __future__ import annotations

from codex_task_runner.gh import gh_api_cli, gh_api_graphql, gh_api_helpers


class GhModule:
    """Aggregates GitHub helpers across the `gh` package."""

    # CLI helpers
    pr_exists_open = staticmethod(gh_api_cli.pr_exists_open)
    create_pr = staticmethod(gh_api_cli.create_pr)
    _parse_created_number = staticmethod(gh_api_cli._parse_created_number)
    merge_pr = staticmethod(gh_api_cli.merge_pr)
    list_branches = staticmethod(gh_api_cli.list_branches)

    # GraphQL helpers
    _pr_graphql_query = staticmethod(gh_api_graphql._pr_graphql_query)
    get_pr = staticmethod(gh_api_graphql.get_pr)
    _parse_pr = staticmethod(gh_api_graphql._parse_pr)
    _checks_state = staticmethod(gh_api_graphql._checks_state)

    # low-level helpers
    _api = staticmethod(gh_api_helpers._api)
    _graphql = staticmethod(gh_api_helpers._graphql)
    _vars = staticmethod(gh_api_helpers._vars)
