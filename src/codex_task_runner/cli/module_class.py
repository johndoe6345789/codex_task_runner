from __future__ import annotations

from codex_task_runner.cli.cli import main
from codex_task_runner.cli.cli_parser import build_parser
from codex_task_runner.cli.cmd_ping import ping_cmd
from codex_task_runner.cli.cmd_poll import poll_cmd
from codex_task_runner.cli.cmd_tasks import tasks_cmd
from codex_task_runner.cli.cmd_task import task_cmd
from codex_task_runner.cli.cmd_turns import turns_cmd
from codex_task_runner.cli.cmd_create_pr import create_pr_cmd
from codex_task_runner.cli.cmd_run import run_cmd


class CliModule:
    """Aggregates CLI entrypoints and implementations for the `cli` package."""

    build_parser = staticmethod(build_parser)
    main = staticmethod(main)
    ping_cmd = staticmethod(ping_cmd)
    poll_cmd = staticmethod(poll_cmd)
    tasks_cmd = staticmethod(tasks_cmd)
    task_cmd = staticmethod(task_cmd)
    turns_cmd = staticmethod(turns_cmd)
    create_pr_cmd = staticmethod(create_pr_cmd)
    run_cmd = staticmethod(run_cmd)
