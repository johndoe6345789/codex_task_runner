import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.codex.codex_tasks_list import get_tasks_list


def test_codex_tasks_list() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_tasks_list._json_get") as mock_get:
        mock_get.return_value = {
            "items": [
                {"id": "t1", "title": "Task 1", "task_status_display": {"environment_label": "o/r", "branch_name": "main"}}
            ]
        }
        result = get_tasks_list(session, limit=10)
        assert len(result) == 1
        assert result[0].task_id == "t1"


def test_codex_tasks_list_empty() -> None:
    session = MagicMock()
    
    with patch("codex_task_runner.codex.codex_tasks_list._json_get") as mock_get:
        mock_get.return_value = None
        result = get_tasks_list(session)
        assert result == []
