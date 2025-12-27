import pytest
from unittest.mock import patch
from codex_task_runner.gh.gh_api_call import gh_api


def test_gh_api_call() -> None:
    with patch("codex_task_runner.gh.gh_api_call.run_ok") as mock_run:
        mock_run.return_value = '{"data": "test"}'
        result = gh_api(["repos/owner/repo"])
        assert result == {"data": "test"}
        mock_run.assert_called_once()
