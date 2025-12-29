import pytest
from unittest.mock import MagicMock, patch
from codex_task_runner.pr.ensure_prs import ensure_prs
from codex_task_runner.etc.task_ref import TaskRef


def test_ensure_prs_with_pr_number_in_response():
    """Test that ensure_prs extracts and returns PR numbers from API response."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-123",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()
    )
    
    with patch("codex_task_runner.pr.ensure_prs.get_turns") as mock_turns, \
         patch("codex_task_runner.pr.ensure_prs.create_pr_for_turn") as mock_create:
        
        mock_turns.return_value = {"current_turn_id": "turn-1"}
        mock_create.return_value = {"pr_url": "https://github.com/owner/repo/pull/42"}
        
        result = ensure_prs(session, [task])
        
        assert result["created"] == 1
        assert result["skipped"] == 0
        assert result["errors"] == []
        assert result["pr_numbers"] == {"task-123": 42}


def test_ensure_prs_with_alternate_url_field():
    """Test that ensure_prs handles 'url' field in addition to 'pr_url'."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-456",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()
    )
    
    with patch("codex_task_runner.pr.ensure_prs.get_turns") as mock_turns, \
         patch("codex_task_runner.pr.ensure_prs.create_pr_for_turn") as mock_create:
        
        mock_turns.return_value = {"current_turn_id": "turn-1"}
        mock_create.return_value = {"url": "https://github.com/owner/repo/pull/99"}
        
        result = ensure_prs(session, [task])
        
        assert result["created"] == 1
        assert result["pr_numbers"] == {"task-456": 99}


def test_ensure_prs_skips_task_with_existing_pr():
    """Test that ensure_prs skips tasks that already have PR numbers."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-789",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=(100,)
    )
    
    with patch("codex_task_runner.pr.ensure_prs.get_turns") as mock_turns, \
         patch("codex_task_runner.pr.ensure_prs.create_pr_for_turn") as mock_create:
        
        result = ensure_prs(session, [task])
        
        assert result["created"] == 0
        assert result["skipped"] == 1
        assert result["pr_numbers"] == {}
        mock_turns.assert_not_called()
        mock_create.assert_not_called()


def test_ensure_prs_handles_no_pr_number_in_url():
    """Test that ensure_prs handles responses without valid PR URL."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-111",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()
    )
    
    with patch("codex_task_runner.pr.ensure_prs.get_turns") as mock_turns, \
         patch("codex_task_runner.pr.ensure_prs.create_pr_for_turn") as mock_create:
        
        mock_turns.return_value = {"current_turn_id": "turn-1"}
        mock_create.return_value = {"pr_url": "https://github.com/owner/repo"}
        
        result = ensure_prs(session, [task])
        
        assert result["created"] == 1
        assert result["pr_numbers"] == {}  # No PR number extracted


def test_ensure_prs_multiple_tasks():
    """Test ensure_prs with multiple tasks."""
    session = MagicMock()
    tasks = [
        TaskRef(
            task_id="task-1",
            title="Task 1",
            repo="owner/repo",
            base_branch="main",
            pr_numbers=()
        ),
        TaskRef(
            task_id="task-2",
            title="Task 2",
            repo="owner/repo",
            base_branch="main",
            pr_numbers=(50,)  # Already has PR
        ),
        TaskRef(
            task_id="task-3",
            title="Task 3",
            repo="owner/repo",
            base_branch="main",
            pr_numbers=()
        ),
    ]
    
    with patch("codex_task_runner.pr.ensure_prs.get_turns") as mock_turns, \
         patch("codex_task_runner.pr.ensure_prs.create_pr_for_turn") as mock_create:
        
        mock_turns.return_value = {"current_turn_id": "turn-1"}
        mock_create.side_effect = [
            {"pr_url": "https://github.com/owner/repo/pull/10"},
            {"pr_url": "https://github.com/owner/repo/pull/20"},
        ]
        
        result = ensure_prs(session, tasks)
        
        assert result["created"] == 2
        assert result["skipped"] == 1
        assert result["pr_numbers"] == {"task-1": 10, "task-3": 20}
