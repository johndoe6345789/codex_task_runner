from typing import Any
from pathlib import Path

from ..codex.codex_poll import poll_urls
from ..codex.codex_save import save_results


def handle(args: Any, session) -> dict:
    urls = Path(args.urls_file).read_text().splitlines()
    res = poll_urls(session, urls)
    save_results(args.out, {"polls": res})
    return {"saved": args.out}
