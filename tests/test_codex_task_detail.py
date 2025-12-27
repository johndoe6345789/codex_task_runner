import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.codex.codex_task_detail import get_task


def test_codex_task_detail() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_task_detail._json_get") as mock_get:
        mock_get.return_value = {"id": "task-123", "title": "Test"}
        result = get_task(session, "task-123")
        assert result == {"id": "task-123", "title": "Test"}


def test_codex_task_detail_not_found() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_task_detail._json_get") as mock_get:
        mock_get.return_value = None
        result = get_task(session, "nonexistent")
        assert result is None
