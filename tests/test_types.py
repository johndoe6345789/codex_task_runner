import pytest
from codex_task_runner.types import TaskRef, PullRequest, MergeMethod, Json


def test_types_exports() -> None:
    # Verify all types are properly exported
    assert TaskRef is not None
    assert PullRequest is not None
    assert MergeMethod is not None
    # Json is a type alias
    sample: Json = {"key": "value"}
    assert isinstance(sample, dict)
