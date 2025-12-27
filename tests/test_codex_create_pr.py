import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.codex.codex_create_pr import create_pr_for_turn


def test_codex_create_pr() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_create_pr._json_post") as mock_post:
        mock_post.return_value = {"pr_url": "http://github.com/pr/1"}
        result = create_pr_for_turn(session, "task-123", "turn-1")
        assert result == {"pr_url": "http://github.com/pr/1"}


def test_codex_create_pr_failure() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_create_pr._json_post") as mock_post:
        mock_post.return_value = None
        result = create_pr_for_turn(session, "task-123", "turn-1")
        assert result is None
