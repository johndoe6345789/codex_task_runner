from __future__ import annotations

from codex_task_runner.cli.cli import main
from codex_task_runner.cli.cli_parser import build_parser
from codex_task_runner.cli import cli_commands


class CliModule:
    """Aggregates CLI entrypoints and implementations for the `cli` package."""

    build_parser = staticmethod(build_parser)
    main = staticmethod(main)
    ping_cmd = staticmethod(cli_commands.ping_cmd)
    poll_cmd = staticmethod(cli_commands.poll_cmd)
    tasks_cmd = staticmethod(cli_commands.tasks_cmd)
    task_cmd = staticmethod(cli_commands.task_cmd)
    turns_cmd = staticmethod(cli_commands.turns_cmd)
    create_pr_cmd = staticmethod(cli_commands.create_pr_cmd)
    run_cmd = staticmethod(cli_commands.run_cmd)
