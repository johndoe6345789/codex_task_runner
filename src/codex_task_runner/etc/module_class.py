from __future__ import annotations

from codex_task_runner.etc import config


class EtcModule:
    """Aggregates configuration helpers."""

    Config = config.Config
    make_config = staticmethod(config.make_config)
