"""Test blocklist functionality."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from codex_task_runner.etc.blocklist import (
    load_blocklist,
    save_blocklist,
    add_to_blocklist,
    remove_from_blocklist,
    is_blocked,
    clear_blocklist,
    list_blocklist
)


@pytest.fixture
def temp_blocklist_path(tmp_path):
    """Use a temporary blocklist file for tests."""
    blocklist_file = tmp_path / "test_blocklist.json"
    with patch("codex_task_runner.etc.blocklist.get_blocklist_path", return_value=blocklist_file):
        yield blocklist_file


def test_load_empty_blocklist(temp_blocklist_path):
    """Test loading blocklist when file doesn't exist."""
    result = load_blocklist()
    assert result == set()


def test_save_and_load_blocklist(temp_blocklist_path):
    """Test saving and loading blocklist."""
    tasks = {"task-123", "task-456", "task-789"}
    save_blocklist(tasks)
    
    loaded = load_blocklist()
    assert loaded == tasks


def test_add_to_blocklist(temp_blocklist_path):
    """Test adding a task to blocklist."""
    result = add_to_blocklist("task-111")
    assert result is True
    
    blocked = load_blocklist()
    assert "task-111" in blocked


def test_add_duplicate_to_blocklist(temp_blocklist_path):
    """Test adding a task that's already blocked."""
    add_to_blocklist("task-222")
    result = add_to_blocklist("task-222")
    
    assert result is False
    blocked = load_blocklist()
    assert blocked == {"task-222"}


def test_remove_from_blocklist(temp_blocklist_path):
    """Test removing a task from blocklist."""
    add_to_blocklist("task-333")
    add_to_blocklist("task-444")
    
    result = remove_from_blocklist("task-333")
    assert result is True
    
    blocked = load_blocklist()
    assert "task-333" not in blocked
    assert "task-444" in blocked


def test_remove_nonexistent_from_blocklist(temp_blocklist_path):
    """Test removing a task that's not in blocklist."""
    result = remove_from_blocklist("task-999")
    assert result is False


def test_is_blocked(temp_blocklist_path):
    """Test checking if a task is blocked."""
    add_to_blocklist("task-555")
    
    assert is_blocked("task-555") is True
    assert is_blocked("task-666") is False


def test_clear_blocklist(temp_blocklist_path):
    """Test clearing all blocklist entries."""
    add_to_blocklist("task-777")
    add_to_blocklist("task-888")
    add_to_blocklist("task-999")
    
    count = clear_blocklist()
    assert count == 3
    
    blocked = load_blocklist()
    assert len(blocked) == 0


def test_list_blocklist(temp_blocklist_path):
    """Test getting sorted list of blocked tasks."""
    add_to_blocklist("task-ccc")
    add_to_blocklist("task-aaa")
    add_to_blocklist("task-bbb")
    
    result = list_blocklist()
    assert result == ["task-aaa", "task-bbb", "task-ccc"]


def test_list_empty_blocklist(temp_blocklist_path):
    """Test listing when blocklist is empty."""
    result = list_blocklist()
    assert result == []
