import pytest
from codex_task_runner.etc.merge_method import MergeMethod


@pytest.mark.parametrize("value,expected", [
    ("merge", MergeMethod.MERGE),
    ("squash", MergeMethod.SQUASH),
    ("rebase", MergeMethod.REBASE),
])
def test_merge_method(value: str, expected: MergeMethod) -> None:
    assert MergeMethod(value) == expected
    assert expected.value == value
