from __future__ import annotations

from codex_task_runner.cli import cli_clean, cli_clean_impl


class CliModule:
    """Aggregates CLI entrypoints and implementations for the `cli` package."""

    make_parser = staticmethod(cli_clean.make_parser)
    main = staticmethod(cli_clean.main)

    ping_cmd = staticmethod(cli_clean_impl.ping_cmd)
    poll_cmd = staticmethod(cli_clean_impl.poll_cmd)
    tasks_cmd = staticmethod(cli_clean_impl.tasks_cmd)
    task_cmd = staticmethod(cli_clean_impl.task_cmd)
    turns_cmd = staticmethod(cli_clean_impl.turns_cmd)
    create_pr_cmd = staticmethod(cli_clean_impl.create_pr_cmd)
    run_cmd = staticmethod(cli_clean_impl.run_cmd)
