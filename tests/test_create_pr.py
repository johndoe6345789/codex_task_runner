import pytest
from codex_task_runner.gh.create_pr import _parse_created_number


@pytest.mark.parametrize("out,expected", [
    ("https://github.com/owner/repo/pull/123", 123),
    ("Created PR https://github.com/owner/repo/pull/42\n", 42),
    ("https://github.com/owner/repo/pull/1 something", 1),
    ("no pull request", None),
    ("", None),
])
def test_create_pr(out: str, expected: int | None) -> None:
    assert _parse_created_number(out) == expected
