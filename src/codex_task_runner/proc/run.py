import subprocess
from .proc_result import ProcResult


def run(cmd: list[str]) -> ProcResult:
    p = subprocess.run(cmd, check=False, text=True, capture_output=True)
    return ProcResult(code=p.returncode, out=p.stdout, err=p.stderr)
