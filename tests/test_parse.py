import pytest
from codex_task_runner.codex.parse_tasks import parse_tasks


@pytest.mark.parametrize("obj,expected_repo,expected_prs", [
    (
        {"items": [{"id": "t1", "title": "X",
                    "task_status_display": {"environment_label": "o/r",
                                           "branch_name": "main"},
                    "pull_requests": []}]},
        "o/r",
        (),
    ),
    (
        {"items": [{"id": "t2", "title": "Y",
                    "task_status_display": {"environment_label": "foo/bar",
                                           "branch_name": "dev"},
                    "pull_requests": []}]},
        "foo/bar",
        (),
    ),
])
def test_parse_tasks(obj: dict, expected_repo: str, expected_prs: tuple) -> None:
    tasks = parse_tasks(obj)
    assert tasks[0].repo == expected_repo
    assert tasks[0].pr_numbers == expected_prs
