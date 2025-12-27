import pytest
from codex_task_runner.codex.parse_tasks import parse_tasks


@pytest.mark.parametrize("obj,expected_count", [
    ({"items": []}, 0),
    ({"items": [{"id": "t1", "title": "X", "task_status_display": {"environment_label": "o/r", "branch_name": "main"}, "pull_requests": []}]}, 1),
    ({"items": [
        {"id": "t1", "title": "X", "task_status_display": {"environment_label": "o/r", "branch_name": "main"}, "pull_requests": []},
        {"id": "t2", "title": "Y", "task_status_display": {"environment_label": "a/b", "branch_name": "dev"}, "pull_requests": []},
    ]}, 2),
])
def test_parse_tasks(obj: dict, expected_count: int) -> None:
    tasks = parse_tasks(obj)
    assert len(tasks) == expected_count
