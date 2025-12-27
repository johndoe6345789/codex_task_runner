import pytest
from codex_task_runner.etc.timeutil import utc_stamp


def test_timeutil() -> None:
    stamp = utc_stamp()
    # Format: YYYYMMDDTHHMMSSZ
    assert len(stamp) == 16
    assert stamp.endswith("Z")
    assert "T" in stamp
