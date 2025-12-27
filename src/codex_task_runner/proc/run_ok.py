from .run import run


def run_ok(cmd: list[str]) -> str:
    r = run(cmd)
    if r.code != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{r.err}")
    return r.out
