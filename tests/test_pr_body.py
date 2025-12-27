import pytest
from codex_task_runner.pr.pr_body import pr_body


@pytest.mark.parametrize("task_id,expected_contains", [
    ("abc123", "abc123"),
    ("task-xyz", "task-xyz"),
    ("", ""),
])
def test_pr_body(task_id: str, expected_contains: str) -> None:
    result = pr_body(task_id)
    assert expected_contains in result
    assert "Codex Task" in result
