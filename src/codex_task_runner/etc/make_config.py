from __future__ import annotations

import pathlib

from .config_class import Config
from .merge_method import MergeMethod
from .default_run_dir import default_run_dir


def make_config(
    require_checks: bool,
    method: str,
    keep_branch: bool,
    admin: bool,
    auto: bool,
    dry_run: bool,
    output_dir: str | None,
) -> Config:
    out = pathlib.Path(output_dir) if output_dir else default_run_dir()
    return Config(
        require_checks=require_checks,
        method=MergeMethod(method),
        delete_branch=not keep_branch,
        admin=admin,
        auto=auto,
        dry_run=dry_run,
        output_dir=out,
    )
