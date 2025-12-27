#!/usr/bin/env python3
from __future__ import annotations

import sys
import pathlib
from codex_task_runner.codex_cloud import session_from_env, poll_urls, save_results


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    env_path = ".env"
    urls_path = "urls.txt"
    out_path = "run_poll.json"
    if len(argv) >= 1:
        urls_path = argv[0]
    if len(argv) >= 2:
        out_path = argv[1]

    if not pathlib.Path(urls_path).exists():
        print(f"urls file not found: {urls_path}")
        return 2

    sess = session_from_env(env_path)
    with open(urls_path, "r", encoding="utf-8") as f:
        urls = [l.strip() for l in f if l.strip()]
    if not urls:
        print("no urls to poll")
        return 3

    # ping main (first) then poll others
    results = {"main": None, "polls": []}
    results["main"] = poll_urls(sess, [urls[0]])[0]
    if len(urls) > 1:
        results["polls"] = poll_urls(sess, urls[1:])

    save_results(out_path, results)
    print(f"saved results to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
