import pytest
from codex_task_runner.etc.slugify import slugify


@pytest.mark.parametrize("input_str,expected", [
    ("Add A, B, and C!", "add-a-b-and-c"),
    ("Hello World", "hello-world"),
    ("foo--bar", "foo-bar"),
    ("", "task"),
])
def test_slugify(input_str: str, expected: str) -> None:
    assert slugify(input_str) == expected
