import pytest
from unittest.mock import patch
from codex_task_runner.gh.gh_graphql import gh_graphql


def test_gh_graphql() -> None:
    with patch("codex_task_runner.gh.gh_graphql.gh_api") as mock_api:
        mock_api.return_value = {"data": {"repository": {}}}
        query = "query { repository { name } }"
        result = gh_graphql(query, {"owner": "o", "name": "r"})
        assert result == {"data": {"repository": {}}}
        mock_api.assert_called_once()
