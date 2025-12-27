from dataclasses import dataclass


@dataclass(frozen=True)
class ProcResult:
    code: int
    out: str
    err: str
