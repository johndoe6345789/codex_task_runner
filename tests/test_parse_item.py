import pytest
from codex_task_runner.codex.codex_parse_item import parse_item


@pytest.mark.parametrize("item,expected_repo,expected_base,expected_title", [
    (
        {"id": "t1", "title": "X", "task_status_display": {"environment_label": "o/r", "branch_name": "main"}, "pull_requests": []},
        "o/r", "main", "X",
    ),
    (
        {"id": "t2", "title": "Y", "task_status_display": {"environment_label": "foo/bar", "branch_name": "dev"}, "pull_requests": []},
        "foo/bar", "dev", "Y",
    ),
    (
        {"id": "t3", "title": "Z", "task_status_display": {}, "pull_requests": []},
        "johndoe6345789/metabuilder", "main", "Z",
    ),
])
def test_parse_item(item: dict, expected_repo: str, expected_base: str, expected_title: str) -> None:
    result = parse_item(item)
    assert result.repo == expected_repo
    assert result.base_branch == expected_base
    assert result.title == expected_title
