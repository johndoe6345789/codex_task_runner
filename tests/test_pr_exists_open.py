import pytest
from unittest.mock import patch
from codex_task_runner.gh.pr_exists_open import pr_exists_open
from codex_task_runner.proc.proc_result import ProcResult


def test_pr_exists_open_found() -> None:
    with patch("codex_task_runner.gh.pr_exists_open.run_ok") as mock_run:
        mock_run.return_value = '[{"number": 42}]'
        result = pr_exists_open("owner/repo", "feature-branch")
        assert result == 42


def test_pr_exists_open_not_found() -> None:
    with patch("codex_task_runner.gh.pr_exists_open.run_ok") as mock_run:
        mock_run.return_value = '[]'
        result = pr_exists_open("owner/repo", "feature-branch")
        assert result is None
