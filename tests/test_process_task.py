import pytest
from unittest.mock import MagicMock, patch, call
from codex_task_runner.pr.process_task import process_task
from codex_task_runner.etc.task_ref import TaskRef


def test_process_task_finds_pr_by_title_after_creation():
    """Test that process_task finds PR by title when API doesn't return PR number."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-123",
        title="Test Task Title",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()
    )
    
    with patch("codex_task_runner.pr.process_task.ensure_prs") as mock_ensure, \
         patch("codex_task_runner.pr.process_task.dedup_handle") as mock_dedup, \
         patch("codex_task_runner.pr.process_task.find_existing_pr") as mock_find, \
         patch("codex_task_runner.pr.process_task.merge_task") as mock_merge:
        
        # First call checks if PR exists (returns None)
        # Second call finds the PR after creation
        mock_find.side_effect = [None, 42]
        
        # ensure_prs returns created but no PR number
        mock_ensure.return_value = {
            "created": 1,
            "skipped": 0,
            "errors": [],
            "pr_numbers": {}  # No PR number in response
        }
        
        # merge succeeds
        mock_merge.return_value = "MERGED PR #42"
        
        result = process_task(session, task, "owner/repo", limit=5, dry_run=False, interactive=False)
        
        # Verify the flow - dedup happens after merge now
        mock_ensure.assert_called_once()
        assert mock_find.call_count == 2  # Called twice
        mock_merge.assert_called_once()
        mock_dedup.assert_called_once()  # Called after merge
        
        # Check result
        assert result["created"] == 1
        assert result["merged"] == 1
        assert result["skipped"] == 0
        assert result["failed"] == 0


def test_process_task_uses_pr_number_from_api():
    """Test that process_task uses PR number directly from API when available."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-456",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()
    )
    
    with patch("codex_task_runner.pr.process_task.ensure_prs") as mock_ensure, \
         patch("codex_task_runner.pr.process_task.dedup_handle") as mock_dedup, \
         patch("codex_task_runner.pr.process_task.find_existing_pr") as mock_find, \
         patch("codex_task_runner.pr.process_task.merge_task") as mock_merge:
        
        # First call checks if PR exists (returns None to trigger creation)
        mock_find.return_value = None
        
        # ensure_prs returns PR number in response
        mock_ensure.return_value = {
            "created": 1,
            "skipped": 0,
            "errors": [],
            "pr_numbers": {"task-456": 99}  # PR number available
        }
        
        # merge succeeds
        mock_merge.return_value = "MERGED PR #99"
        
        result = process_task(session, task, "owner/repo", limit=5, dry_run=False, interactive=False)
        
        # Verify the flow - dedup happens after merge now
        mock_ensure.assert_called_once()
        assert mock_find.call_count == 1  # Only initial check
        mock_merge.assert_called_once()
        mock_dedup.assert_called_once()  # Called after merge
        
        # Check result
        assert result["created"] == 1
        assert result["merged"] == 1


def test_process_task_with_existing_pr():
    """Test that process_task skips creation if PR already exists."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-789",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=(100,)  # Already has PR
    )
    
    with patch("codex_task_runner.pr.process_task.ensure_prs") as mock_ensure, \
         patch("codex_task_runner.pr.process_task.dedup_handle") as mock_dedup, \
         patch("codex_task_runner.pr.process_task.merge_task") as mock_merge:
        
        mock_merge.return_value = "MERGED PR #100"
        
        result = process_task(session, task, "owner/repo", limit=5, dry_run=False, interactive=False)
        
        # Should NOT call ensure_prs since PR already exists
        mock_ensure.assert_not_called()
        mock_merge.assert_called_once()
        mock_dedup.assert_called_once()  # Dedup still runs after merge
        
        # Check result
        assert result["created"] == 0
        assert result["merged"] == 1


def test_process_task_finds_existing_pr_on_github():
    """Test that process_task finds PR that exists on GitHub but not in task."""
    session = MagicMock()
    task = TaskRef(
        task_id="task-111",
        title="Test Task",
        repo="owner/repo",
        base_branch="main",
        pr_numbers=()  # No PR in task
    )
    
    with patch("codex_task_runner.pr.process_task.find_existing_pr") as mock_find, \
         patch("codex_task_runner.pr.process_task.ensure_prs") as mock_ensure, \
         patch("codex_task_runner.pr.process_task.dedup_handle") as mock_dedup, \
         patch("codex_task_runner.pr.process_task.merge_task") as mock_merge:
        
        # First call finds existing PR on GitHub
        mock_find.return_value = 50
        mock_merge.return_value = "MERGED PR #50"
        
        result = process_task(session, task, "owner/repo", limit=5, dry_run=False, interactive=False)
        
        # Should find existing PR before trying to create
        mock_find.assert_called_once_with("owner/repo", "Test Task")
        mock_ensure.assert_not_called()  # Should skip creation
        mock_merge.assert_called_once()
        mock_dedup.assert_called_once()  # Dedup still runs after merge
        
        # Check result
        assert result["created"] == 0
        assert result["merged"] == 1
