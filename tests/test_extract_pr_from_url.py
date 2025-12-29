import pytest
from codex_task_runner.pr.ensure_prs import _extract_pr_number_from_url


@pytest.mark.parametrize("url,expected", [
    ("https://github.com/owner/repo/pull/123", 123),
    ("http://github.com/owner/repo/pull/456", 456),
    ("https://github.com/user/project/pull/1", 1),
    ("https://github.com/org/repo/pull/9999", 9999),
    ("", None),
    (None, None),
    ("https://github.com/owner/repo", None),
    ("https://github.com/owner/repo/issues/123", None),
    ("not a url", None),
])
def test_extract_pr_number_from_url(url, expected):
    assert _extract_pr_number_from_url(url) == expected
