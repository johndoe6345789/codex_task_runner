import pytest
from unittest.mock import patch
from codex_task_runner.pr.first_open import _first_open
from codex_task_runner.etc.pull_request import PullRequest


def test_first_open_found() -> None:
    with patch("codex_task_runner.pr.first_open.get_pr") as mock_get:
        mock_get.return_value = PullRequest(number=1, url="http://gh/1", title="T", author="a", mergeable="MERGEABLE", checks_state="SUCCESS")
        result = _first_open("owner/repo", [1, 2])
        assert result == 1


def test_first_open_not_mergeable() -> None:
    with patch("codex_task_runner.pr.first_open.get_pr") as mock_get:
        mock_get.side_effect = [
            PullRequest(number=1, url="http://gh/1", title="T", author="a", mergeable="", checks_state=None),
            PullRequest(number=2, url="http://gh/2", title="T2", author="b", mergeable="MERGEABLE", checks_state="SUCCESS"),
        ]
        result = _first_open("owner/repo", [1, 2])
        assert result == 2


def test_first_open_all_fail() -> None:
    with patch("codex_task_runner.pr.first_open.get_pr") as mock_get:
        mock_get.side_effect = Exception("Not found")
        result = _first_open("owner/repo", [1, 2])
        assert result is None


def test_first_open_empty() -> None:
    result = _first_open("owner/repo", [])
    assert result is None
