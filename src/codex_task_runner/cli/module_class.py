from __future__ import annotations

from codex_task_runner.cli import cli_legacy, cli_commands


class CliModule:
    """Aggregates CLI entrypoints and implementations for the `cli` package."""

    make_parser = staticmethod(cli_legacy.make_parser)
    main = staticmethod(cli_legacy.main)

    ping_cmd = staticmethod(cli_commands.ping_cmd)
    poll_cmd = staticmethod(cli_commands.poll_cmd)
    tasks_cmd = staticmethod(cli_commands.tasks_cmd)
    task_cmd = staticmethod(cli_commands.task_cmd)
    turns_cmd = staticmethod(cli_commands.turns_cmd)
    create_pr_cmd = staticmethod(cli_commands.create_pr_cmd)
    run_cmd = staticmethod(cli_commands.run_cmd)
