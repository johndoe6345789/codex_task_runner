import pytest
from codex_task_runner.proc.proc_result import ProcResult


@pytest.mark.parametrize("code,out,err", [
    (0, "output", ""),
    (1, "", "error"),
    (127, "mixed", "also mixed"),
])
def test_proc_result(code, out, err) -> None:
    r = ProcResult(code=code, out=out, err=err)
    assert r.code == code
    assert r.out == out
    assert r.err == err
