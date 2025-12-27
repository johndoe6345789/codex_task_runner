import pytest
from codex_task_runner.codex.load_tasks import load_tasks


@pytest.mark.parametrize("raw,expected_count", [
    ('{"items": []}', 0),
    ('{"items": [{"id": "t1", "title": "X", "task_status_display": {"environment_label": "o/r", "branch_name": "main"}, "pull_requests": []}]}', 1),
])
def test_load_tasks(raw: str, expected_count: int) -> None:
    tasks = load_tasks(raw)
    assert len(tasks) == expected_count
