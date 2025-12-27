import pytest
import re
from codex_task_runner.etc.timeutil import utc_stamp


def test_utc_stamp() -> None:
    result = utc_stamp()
    # Format: YYYYMMDDTHHMMSSZ
    assert re.match(r"^\d{8}T\d{6}Z$", result)
    assert result.endswith("Z")
