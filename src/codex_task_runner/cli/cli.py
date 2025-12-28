#!/usr/bin/env python3
import json
from pathlib import Path

from codex_task_runner.codex.codex_session import session_from_env
from codex_task_runner.handlers import ping, poll, tasks, task, turns, create_pr, run, yolo, dedup_prs, discover, archive, patch, me, ui, prompt
from .cli_parser import build_parser

# Map command names to handler modules
_HANDLERS = {
    "ping": ping,
    "poll": poll,
    "tasks": tasks,
    "task": task,
    "turns": turns,
    "create-pr": create_pr,
    "run": run,
    "yolo": yolo,
    "dedup-prs": dedup_prs,
    "discover": discover,
    "archive": archive,
    "patch": patch,
    "me": me,
    "ui": ui,
    "prompt": prompt,
    # Aliases
    "ls": tasks,
    "list": tasks,
    "t": task,
    "show": task,
    "pr": create_pr,
    "go": yolo,
    "auto": yolo,
    "dedup": dedup_prs,
    "whoami": me,
    "done": archive,
    "close": archive,
    "diff": patch,
    "p": patch,
    "gui": ui,
    "app": ui,
    "send": prompt,
    "new": prompt,
}


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else None
    map_path = Path(__file__).parent / "cli_map.json"
    parser = build_parser(map_path)
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 1

    session = session_from_env(getattr(args, "env", ".env"))

    handler = _HANDLERS.get(args.cmd)
    if not handler:
        print(f"No handler configured for command: {args.cmd}")
        return 2
    if not hasattr(handler, "handle"):
        print("Handler missing 'handle' function.")
        return 3
    result = handler.handle(args, session)
    try:
        print(json.dumps(result, indent=2))
    except TypeError:
        print(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
