#!/usr/bin/env python3
import importlib
import json
from pathlib import Path
from typing import Any

from .codex_cloud import session_from_env
from .cli_parser import build_parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else None
    map_path = Path(__file__).parent / "cli_map.json"
    parser = build_parser(map_path)
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 1

    session = session_from_env(getattr(args, "env", ".env"))

    handler_path = getattr(args, "_handler", None)
    if not handler_path:
        print("No handler configured for this command.")
        return 2
    mod = importlib.import_module(handler_path)
    if not hasattr(mod, "handle"):
        print("Handler missing 'handle' function.")
        return 3
    result = mod.handle(args, session)
    try:
        print(json.dumps(result, indent=2))
    except TypeError:
        print(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
