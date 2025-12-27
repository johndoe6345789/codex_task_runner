import pytest
from codex_task_runner.codex.codex_parse_cookie import parse_cookie_string


@pytest.mark.parametrize("cookie_str,expected_keys", [
    ("", []),
    ("foo=bar", ["foo"]),
    ("foo=bar; baz=qux", ["foo", "baz"]),
    ("a=1; b=2; c=3", ["a", "b", "c"]),
])
def test_parse_cookie_string(cookie_str: str, expected_keys: list) -> None:
    jar = parse_cookie_string(cookie_str)
    for key in expected_keys:
        assert key in [c.name for c in jar]
