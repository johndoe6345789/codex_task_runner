from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcResult:
    code: int
    out: str
    err: str


def run(cmd: list[str]) -> ProcResult:
    p = subprocess.run(cmd, check=False, text=True, capture_output=True)
    return ProcResult(code=p.returncode, out=p.stdout, err=p.stderr)


def run_ok(cmd: list[str]) -> str:
    r = run(cmd)
    if r.code != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{r.err}")
    return r.out
