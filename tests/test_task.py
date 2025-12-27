import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.handlers.task import handle


def test_task_handler() -> None:
    args = MagicMock()
    args.task_id = "task-123"
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.task.get_task") as mock_get:
        mock_get.return_value = {"id": "task-123", "title": "Test"}
        result = handle(args, session)
        assert result == {"id": "task-123", "title": "Test"}


def test_task_handler_not_found() -> None:
    args = MagicMock()
    args.task_id = "nonexistent"
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.task.get_task") as mock_get:
        mock_get.return_value = None
        result = handle(args, session)
        assert result is None
