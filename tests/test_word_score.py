import pytest
from codex_task_runner.branch.word_score import word_score


@pytest.mark.parametrize("branch,words_set,expected", [
    ("feature-add-button", {"add", "button"}, 2),
    ("feature-add-button", {"add"}, 1),
    ("feature-add-button", {"foo", "bar"}, 0),
    ("codex/fix-bug-123", {"fix", "bug"}, 2),
    ("main", {"main"}, 1),
])
def test_word_score(branch: str, words_set: set, expected: int) -> None:
    assert word_score(branch, words_set) == expected
