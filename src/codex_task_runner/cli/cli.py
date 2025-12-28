#!/usr/bin/env python3
import json
from pathlib import Path

from codex_task_runner.codex.codex_session import session_from_env
from codex_task_runner.handlers import (
    ping, poll, tasks, task, turns, create_pr, run, yolo, 
    dedup_prs, discover, archive, patch, me, ui, prompt, serve
)
from codex_task_runner import cli_helpers
from types import SimpleNamespace
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
    "serve": serve,
}

# Add common aliases
_ALIASES = {
    "ls": "tasks",
    "list": "tasks",
    "t": "task",
    "show": "task",
    "pr": "create-pr",
    "go": "yolo",
    "auto": "yolo",
    "dedup": "dedup-prs",
    "whoami": "me",
    "done": "archive",
    "close": "archive",
    "diff": "patch",
    "p": "patch",
    "gui": "ui",
    "app": "ui",
    "send": "prompt",
    "new": "prompt",
    "server": "serve",
    "api": "serve",
    "flask": "serve",
}

# CLI helper adapters
def _convert_md_adapter(args, session):
    p = cli_helpers.convert_md_to_wikitext(getattr(args, "src", None), getattr(args, "dest", None))
    return str(p)


def _publish_mcp_adapter(args, session):
    return cli_helpers.publish_to_wiki(
        getattr(args, "username"),
        getattr(args, "password"),
        title=getattr(args, "title", "MCP Integration"),
        docpath=getattr(args, "docpath", None),
        api=getattr(args, "api", "http://localhost:8080/api.php"),
    )


def _compute_coverage_adapter(args, session):
    react_glob = getattr(args, "react_glob", None)
    if react_glob == []:
        react_glob = None
    return cli_helpers.compute_coverage(getattr(args, "qmldir", None), react_glob)


def _poll_codex_adapter(args, session):
    env = getattr(args, "env", ".env")
    urls_file = getattr(args, "urls_file", "urls.txt")
    out = getattr(args, "out", "run_poll.json")
    return str(cli_helpers.poll_codex_urls(env, urls_file, out))


def _run_to_github_adapter(args, session):
    env = getattr(args, "env", ".env")
    dry_run = getattr(args, "dry_run", False)
    limit = getattr(args, "limit", 20)
    return cli_helpers.run_codex_to_github(env, dry_run, limit)


# Extended command handlers
_EXTENDED_HANDLERS = {
    "convert-md": SimpleNamespace(handle=_convert_md_adapter),
    "md-to-wiki": SimpleNamespace(handle=_convert_md_adapter),
    "publish-mcp": SimpleNamespace(handle=_publish_mcp_adapter),
    "publish-wiki": SimpleNamespace(handle=_publish_mcp_adapter),
    "publish-mw": SimpleNamespace(handle=_publish_mcp_adapter),
    "compute-coverage": SimpleNamespace(handle=_compute_coverage_adapter),
    "coverage": SimpleNamespace(handle=_compute_coverage_adapter),
    "poll-codex": SimpleNamespace(handle=_poll_codex_adapter),
    "poll-urls": SimpleNamespace(handle=_poll_codex_adapter),
    "run-to-github": SimpleNamespace(handle=_run_to_github_adapter),
    "run-codex": SimpleNamespace(handle=_run_to_github_adapter),
    "run-to-gh": SimpleNamespace(handle=_run_to_github_adapter),
}


def main(argv: list[str] | None = None) -> int:
    """Main entry point for CLI."""
    argv = list(argv) if argv is not None else None
    map_path = Path(__file__).parent / "cli_map.json"
    parser = build_parser(map_path)
    args = parser.parse_args(argv)
    
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 1

    # Create session
    session = session_from_env(getattr(args, "env", ".env"))

    # Resolve command (handle aliases)
    cmd = _ALIASES.get(args.cmd, args.cmd)
    
    # Find handler
    handler = _HANDLERS.get(cmd) or _EXTENDED_HANDLERS.get(cmd)
    if not handler:
        print(f"No handler configured for command: {args.cmd}")
        return 2
    if not hasattr(handler, "handle"):
        print("Handler missing 'handle' function.")
        return 3
    
    # Execute and print result
    result = handler.handle(args, session)
    try:
        print(json.dumps(result, indent=2))
    except TypeError:
        print(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
