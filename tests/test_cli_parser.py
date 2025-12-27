import pytest
from pathlib import Path
from codex_task_runner.cli.cli_parser import build_parser


def test_cli_parser() -> None:
    map_path = Path(__file__).parent.parent / "src" / "codex_task_runner" / "cli" / "cli_map.json"
    parser = build_parser(map_path)
    assert parser is not None
    
    # Test parsing a simple command
    args = parser.parse_args(["ping", "http://example.com"])
    assert args.cmd == "ping"
    assert args.url == "http://example.com"


def test_cli_parser_tasks() -> None:
    map_path = Path(__file__).parent.parent / "src" / "codex_task_runner" / "cli" / "cli_map.json"
    parser = build_parser(map_path)
    
    args = parser.parse_args(["tasks"])
    assert args.cmd == "tasks"
