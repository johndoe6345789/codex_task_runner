from __future__ import annotations

import pathlib
from dataclasses import dataclass

from .merge_method import MergeMethod


@dataclass(frozen=True)
class Config:
    require_checks: bool
    method: MergeMethod
    delete_branch: bool
    admin: bool
    auto: bool
    dry_run: bool
    output_dir: pathlib.Path


def make_config(
    require_checks: bool,
    method: str,
    keep_branch: bool,
    admin: bool,
    auto: bool,
    dry_run: bool,
    output_dir: str | None,
) -> Config:
    out = pathlib.Path(output_dir) if output_dir else pathlib.Path(".")
    return Config(
        require_checks=require_checks,
        method=MergeMethod(method),
        delete_branch=not keep_branch,
        admin=admin,
        auto=auto,
        dry_run=dry_run,
        output_dir=out,
    )
