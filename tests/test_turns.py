import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.handlers.turns import handle


def test_turns_handler() -> None:
    args = MagicMock()
    args.task_id = "task-123"
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.turns.get_turns") as mock_get:
        mock_get.return_value = {"turns": [{"id": 1}]}
        result = handle(args, session)
        assert result == {"turns": [{"id": 1}]}


def test_turns_handler_not_found() -> None:
    args = MagicMock()
    args.task_id = "nonexistent"
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.turns.get_turns") as mock_get:
        mock_get.return_value = None
        result = handle(args, session)
        assert result is None
