#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TYPE_MAP = {"int": int, "str": str, "float": float}


def build_parser(map_path: Path) -> argparse.ArgumentParser:
    doc = json.loads(map_path.read_text())
    p = argparse.ArgumentParser(prog="codex-runner")
    p.add_argument("--env", default=".env", help="Path to .env with cookies/tokens")
    sub = p.add_subparsers(dest="cmd")
    for cmd in doc.get("commands", []):
        name = cmd["name"]
        sp = sub.add_parser(name, help=cmd.get("help"))
        for arg in cmd.get("args", []):
            flags = arg.get("flags", [])
            kwargs = arg.get("kwargs", {})
            if "type" in kwargs and isinstance(kwargs["type"], str):
                kwargs["type"] = TYPE_MAP.get(kwargs["type"], str)
            if len(flags) == 1 and not flags[0].startswith("-"):
                sp.add_argument(flags[0], **kwargs)
            else:
                sp.add_argument(*flags, **kwargs)
        sp.set_defaults(_handler=cmd.get("handler"))
    return p
