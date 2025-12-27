import pytest
from codex_task_runner.gh.gh_vars import gh_vars


@pytest.mark.parametrize("repo,number,expected", [
    ("owner/repo", 1, {"owner": "owner", "name": "repo", "number": 1}),
    ("foo/bar", 42, {"owner": "foo", "name": "bar", "number": 42}),
    ("org/project", 100, {"owner": "org", "name": "project", "number": 100}),
])
def test_gh_vars(repo: str, number: int, expected: dict) -> None:
    assert gh_vars(repo, number) == expected
