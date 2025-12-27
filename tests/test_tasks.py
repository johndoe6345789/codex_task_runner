import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.handlers.tasks import handle
from codex_task_runner.etc.task_ref import TaskRef


def test_tasks_handler() -> None:
    args = MagicMock()
    args.limit = 10
    session = MagicMock()
    
    mock_task = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    
    with patch("codex_task_runner.handlers.tasks.get_tasks_list") as mock_get:
        mock_get.return_value = [mock_task]
        result = handle(args, session)
        assert len(result) == 1
        assert result[0]["task_id"] == "t1"


def test_tasks_handler_empty() -> None:
    args = MagicMock()
    session = MagicMock()
    
    with patch("codex_task_runner.handlers.tasks.get_tasks_list") as mock_get:
        mock_get.return_value = []
        result = handle(args, session)
        assert result == []
