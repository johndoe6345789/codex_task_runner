import pytest
from unittest.mock import patch
from codex_task_runner.gh.list_branches import list_branches
from codex_task_runner.proc.proc_result import ProcResult


def test_list_branches_success() -> None:
    with patch("codex_task_runner.gh.list_branches.run") as mock_run:
        mock_run.return_value = ProcResult(code=0, out='[{"name": "main"}, {"name": "dev"}]', err="")
        result = list_branches("owner/repo", limit=100)
        assert result == ["main", "dev"]


def test_list_branches_not_found() -> None:
    with patch("codex_task_runner.gh.list_branches.run") as mock_run:
        mock_run.return_value = ProcResult(code=1, out="", err="Not Found (HTTP 404)")
        result = list_branches("owner/repo", limit=100)
        assert result == []


def test_list_branches_error() -> None:
    with patch("codex_task_runner.gh.list_branches.run") as mock_run:
        mock_run.return_value = ProcResult(code=1, out="", err="Some other error")
        with pytest.raises(RuntimeError):
            list_branches("owner/repo", limit=100)
