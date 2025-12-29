"""Tests for find_existing_pr function."""
import pytest
from unittest.mock import patch, MagicMock
from codex_task_runner.pr.find_existing_pr import find_existing_pr


def test_find_existing_pr_by_title():
    """Test finding PR by exact title match."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = """[
            {"number": 42, "title": "Add feature X", "headRefName": "codex/add-feature-x"},
            {"number": 43, "title": "Fix bug Y", "headRefName": "codex/fix-bug-y"}
        ]"""
        mock_run.return_value = mock_result
        
        result = find_existing_pr("owner/repo", "Add feature X")
        assert result == 42


def test_find_existing_pr_by_branch_exact():
    """Test finding PR by exact branch name match."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = """[
            {"number": 379, "title": "test: reorganize hook tests", "headRefName": "codex/create-and-organize-test-files"}
        ]"""
        mock_run.return_value = mock_result
        
        # Task title doesn't match PR title, but branch name should match
        result = find_existing_pr("owner/repo", "Create and organize test files")
        assert result == 379


def test_find_existing_pr_by_branch_with_suffix():
    """Test finding PR by branch name with random suffix."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = """[
            {"number": 100, "title": "Some different title", "headRefName": "codex/create-and-organize-test-files-abc123"}
        ]"""
        mock_run.return_value = mock_result
        
        # Should match even with random suffix
        result = find_existing_pr("owner/repo", "Create and organize test files")
        assert result == 100


def test_find_existing_pr_by_normalized_title():
    """Test finding PR by normalized title (handles punctuation/spacing)."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = """[
            {"number": 50, "title": "Add MenuItemList, Header, and NavSections", "headRefName": "codex/add-items"}
        ]"""
        mock_run.return_value = mock_result
        
        # Punctuation differences should still match
        result = find_existing_pr("owner/repo", "Add MenuItemList Header and NavSections")
        assert result == 50


def test_find_existing_pr_not_found():
    """Test when no matching PR exists."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = """[
            {"number": 10, "title": "Something else", "headRefName": "codex/other"}
        ]"""
        mock_run.return_value = mock_result
        
        result = find_existing_pr("owner/repo", "Non-existent task")
        assert result is None


def test_find_existing_pr_gh_command_fails():
    """Test when gh command fails."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 1
        mock_result.err = "Error: not authorized"
        mock_run.return_value = mock_result
        
        result = find_existing_pr("owner/repo", "Some task")
        assert result is None


def test_find_existing_pr_invalid_json():
    """Test when gh returns invalid JSON."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        mock_result.out = "not valid json"
        mock_run.return_value = mock_result
        
        result = find_existing_pr("owner/repo", "Some task")
        assert result is None


def test_find_existing_pr_real_world_case():
    """Test with real-world example from the issue."""
    with patch("codex_task_runner.pr.find_existing_pr.run") as mock_run:
        mock_result = MagicMock()
        mock_result.code = 0
        # This is the actual scenario from the user's output
        mock_result.out = """[
            {"number": 379, "title": "test: reorganize hook tests", "headRefName": "codex/create-and-organize-test-files"},
            {"number": 380, "title": "Refactor sonner toast components", "headRefName": "codex/create-toastcontainer-and-config-files"},
            {"number": 381, "title": "Refactor sidebar navigation components into smaller files", "headRefName": "codex/add-menuitemlist,-header,-and-navsections"},
            {"number": 382, "title": "Split dialog components into smaller modules", "headRefName": "codex/split-components-into-separate-files"},
            {"number": 383, "title": "Add shared data form and table components", "headRefName": "codex/create-fieldgroup-and-validationsummary-components"}
        ]"""
        mock_run.return_value = mock_result
        
        # All these should find their respective PRs by branch name
        assert find_existing_pr("owner/repo", "Create and organize test files") == 379
        assert find_existing_pr("owner/repo", "Create ToastContainer and config files") == 380
        assert find_existing_pr("owner/repo", "Add MenuItemList, Header, and NavSections") == 381
        assert find_existing_pr("owner/repo", "Split components into separate files") == 382
        assert find_existing_pr("owner/repo", "Create FieldGroup and ValidationSummary components") == 383
