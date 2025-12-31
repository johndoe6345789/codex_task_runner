"""Test interactive conflict menu."""
import pytest
from unittest.mock import patch, MagicMock
from codex_task_runner.etc.conflict_menu import show_conflict_menu, show_conflict_actions, get_conflict_summary


def test_show_conflict_menu_followup(monkeypatch):
    """Test menu returns 'followup' when user chooses 1."""
    task = MagicMock()
    task.title = "Test task"
    
    # Mock input to return "1"
    monkeypatch.setattr('builtins.input', lambda _: "1")
    
    result = show_conflict_menu(task, 123, "merge conflicts")
    assert result == "followup"


def test_show_conflict_menu_skip(monkeypatch):
    """Test menu returns 'skip' when user chooses 2."""
    task = MagicMock()
    task.title = "Test task"
    
    monkeypatch.setattr('builtins.input', lambda _: "2")
    
    result = show_conflict_menu(task, 123, "CI failure")
    assert result == "skip"


def test_show_conflict_menu_invalid_then_valid(monkeypatch):
    """Test menu handles invalid input then valid."""
    task = MagicMock()
    task.title = "Test task"
    
    inputs = iter(["invalid", "99", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    result = show_conflict_menu(task, 123, "not mergeable")
    assert result == "view"


def test_show_conflict_menu_abort(monkeypatch):
    """Test menu returns 'abort' when user chooses 5."""
    task = MagicMock()
    task.title = "Test task"
    
    monkeypatch.setattr('builtins.input', lambda _: "5")
    
    result = show_conflict_menu(task, 123, "some error")
    assert result == "abort"


def test_show_conflict_menu_blocklist(monkeypatch):
    """Test menu returns 'blocklist' when user chooses 6."""
    task = MagicMock()
    task.title = "Test task"
    
    monkeypatch.setattr('builtins.input', lambda _: "6")
    
    result = show_conflict_menu(task, 456, "persistent issue")
    assert result == "blocklist"


def test_show_conflict_menu_accept_incoming(monkeypatch):
    """Test menu returns 'accept_incoming' when user chooses 7."""
    task = MagicMock()
    task.title = "Test task"
    
    monkeypatch.setattr('builtins.input', lambda _: "7")
    
    result = show_conflict_menu(task, 789, "merge conflicts")
    assert result == "accept_incoming"


def test_show_conflict_actions():
    """Test that show_conflict_actions runs without error."""
    # This function prints to stdout, just verify it doesn't crash
    show_conflict_actions("https://github.com/user/repo/pull/123", "merge conflicts")
    show_conflict_actions("https://github.com/user/repo/pull/123", "CI checks: FAILURE")
    show_conflict_actions("https://github.com/user/repo/pull/123", "not mergeable")


def test_get_conflict_summary_empty():
    """Test summary with no conflicts."""
    result = get_conflict_summary([])
    assert "No conflicts encountered" in result


def test_get_conflict_summary_with_conflicts():
    """Test summary with multiple conflicts."""
    task1 = MagicMock()
    task1.title = "Task 1"
    task2 = MagicMock()
    task2.title = "Task 2"
    
    conflicts = [
        (task1, 123, "merge conflicts"),
        (task2, 456, "CI failure"),
    ]
    
    result = get_conflict_summary(conflicts)
    assert "2 PRs blocked" in result
    assert "PR #123" in result
    assert "PR #456" in result
    assert "Task 1" in result
    assert "Task 2" in result
