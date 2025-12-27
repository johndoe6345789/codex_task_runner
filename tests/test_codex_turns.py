import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.codex.codex_turns import get_turns


def test_codex_turns() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_turns._json_get") as mock_get:
        mock_get.return_value = {"turns": [{"id": 1}, {"id": 2}]}
        result = get_turns(session, "task-123")
        assert result == {"turns": [{"id": 1}, {"id": 2}]}


def test_codex_turns_not_found() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_turns._json_get") as mock_get:
        mock_get.return_value = None
        result = get_turns(session, "nonexistent")
        assert result is None
