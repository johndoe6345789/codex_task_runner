import pytest
from codex_task_runner.types import PullRequest
from codex_task_runner.process.is_clean import is_clean


@pytest.mark.parametrize("mergeable,checks_state,require_checks,expected", [
    ("MERGEABLE", "SUCCESS", True, True),
    ("MERGEABLE", "SUCCESS", False, True),
    ("MERGEABLE", "FAILURE", True, False),
    ("MERGEABLE", "FAILURE", False, True),
    ("CONFLICTING", "SUCCESS", True, False),
    ("CONFLICTING", "SUCCESS", False, False),
    ("UNKNOWN", "SUCCESS", True, False),
])
def test_is_clean(mergeable: str, checks_state: str, require_checks: bool, expected: bool) -> None:
    pr = PullRequest(number=1, url="http://x", title="T", author="a", mergeable=mergeable, checks_state=checks_state)
    assert is_clean(pr, require_checks) == expected
