import pytest
from codex_task_runner.gh.get_pr import _parse_pr, _checks_state


@pytest.mark.parametrize("node,expected_number,expected_mergeable", [
    (
        {"number": 1, "title": "T", "url": "http://gh/1", "author": {"login": "alice"}, "mergeable": "MERGEABLE", "commits": None},
        1, "MERGEABLE",
    ),
    (
        {"number": 42, "title": "Fix", "url": "http://gh/42", "author": {"login": "bob"}, "mergeable": None, "commits": None},
        42, "",
    ),
])
def test_get_pr_parse(node, expected_number, expected_mergeable) -> None:
    pr = _parse_pr(node)
    assert pr.number == expected_number
    assert pr.mergeable == expected_mergeable


@pytest.mark.parametrize("commits,expected", [
    (None, None),
    ({}, None),
    ({"nodes": []}, None),
    ({"nodes": [{"commit": {"statusCheckRollup": {"state": "SUCCESS"}}}]}, "SUCCESS"),
    ({"nodes": [{"commit": {"statusCheckRollup": None}}]}, None),
])
def test_checks_state(commits, expected) -> None:
    assert _checks_state(commits) == expected
