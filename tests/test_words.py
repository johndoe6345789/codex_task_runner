import pytest
from codex_task_runner.etc.words import words


@pytest.mark.parametrize("input_str,expected", [
    ("Hello, World!", ["hello", "world"]),
    ("foo-bar_baz", ["foo", "bar", "baz"]),
    ("CamelCase", ["camelcase"]),
    ("", []),
])
def test_words(input_str: str, expected: list[str]) -> None:
    assert words(input_str) == expected
