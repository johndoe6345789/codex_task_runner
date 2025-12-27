import pytest
from codex_task_runner.codex.extract_pr_numbers import extract_pr_numbers


@pytest.mark.parametrize("pull_requests,expected", [
    ([], []),
    (None, []),
    ("invalid", []),
    ([{"pull_request": {"number": 1}}], [1]),
    ([{"pull_request": {"number": 1}}, {"pull_request": {"number": 2}}], [1, 2]),
    ([{"pull_request": {"number": 1}}, {"other": "data"}], [1]),
    ([{"pull_request": None}], []),
])
def test_extract_pr_numbers(pull_requests, expected: list) -> None:
    assert extract_pr_numbers(pull_requests) == expected
