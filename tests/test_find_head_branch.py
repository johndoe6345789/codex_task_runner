import pytest
from unittest.mock import patch
from codex_task_runner.branch.find_head_branch import find_head_branch


def test_find_head_branch_direct_match() -> None:
    with patch("codex_task_runner.branch.find_head_branch.list_branches") as mock_list:
        mock_list.return_value = ["main", "codex/add-button"]
        result = find_head_branch("o/r", "Add button", "task123")
        assert result == "codex/add-button"


def test_find_head_branch_fuzzy_match() -> None:
    with patch("codex_task_runner.branch.find_head_branch.list_branches") as mock_list:
        with patch("codex_task_runner.branch.find_head_branch.fuzzy_branch") as mock_fuzzy:
            mock_list.return_value = ["main", "codex/something-else"]
            mock_fuzzy.return_value = "codex/something-else"
            result = find_head_branch("o/r", "Different title", "task123")
            assert result == "codex/something-else"


def test_find_head_branch_not_found() -> None:
    with patch("codex_task_runner.branch.find_head_branch.list_branches") as mock_list:
        with patch("codex_task_runner.branch.find_head_branch.fuzzy_branch") as mock_fuzzy:
            mock_list.return_value = ["main"]
            mock_fuzzy.return_value = None
            result = find_head_branch("o/r", "No match", "task123")
            assert result is None
