#!/usr/bin/env python3
import argparse
#!/usr/bin/env python3
import argparse
import importlib
import json
from pathlib import Path
from typing import Any

from .codex_cloud import session_from_env


TYPE_MAP = {"int": int, "str": str, "float": float}


def _add_arg(sp: argparse.ArgumentParser, arg: dict) -> None:
    flags = arg.get("flags", [])
    kwargs = dict(arg.get("kwargs", {}))
    # translate type string to real type
    t = kwargs.get("type")
    if isinstance(t, str) and t in TYPE_MAP:
        kwargs["type"] = TYPE_MAP[t]
    # JSON `null` -> Python None already handled by json loader
    sp.add_argument(*flags if all(f.startswith("-") for f in flags) else flags[0], **kwargs) if len(flags) == 1 and not flags[0].startswith("-") else sp.add_argument(*flags, **kwargs)


def build_parser(map_path: Path) -> argparse.ArgumentParser:
    doc = json.loads(map_path.read_text())
    p = argparse.ArgumentParser(prog="codex-runner")
    p.add_argument("--env", default=".env", help="Path to .env with cookies/tokens")
    sub = p.add_subparsers(dest="cmd")
    for cmd in doc.get("commands", []):
        name = cmd["name"]
        sp = sub.add_parser(name, help=cmd.get("help"))
        for arg in cmd.get("args", []):
            # Normalize flags: positional when first flag has no leading '-'
            flags = arg.get("flags", [])
            kwargs = arg.get("kwargs", {})
            # handle type names
            if "type" in kwargs and isinstance(kwargs["type"], str):
                kwargs["type"] = TYPE_MAP.get(kwargs["type"], str)
            if len(flags) == 1 and not flags[0].startswith("-"):
                sp.add_argument(flags[0], **kwargs)
            else:
                sp.add_argument(*flags, **kwargs)
        # attach handler module path for dispatch
        sp.set_defaults(_handler=cmd.get("handler"))
    return p


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
        if args.dry_run:
