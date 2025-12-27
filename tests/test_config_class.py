import pytest
from pathlib import Path
from codex_task_runner.etc.config_class import Config
from codex_task_runner.etc.merge_method import MergeMethod


@pytest.mark.parametrize("require_checks,method,delete_branch,admin,auto,dry_run", [
    (True, MergeMethod.MERGE, True, False, False, True),
    (False, MergeMethod.SQUASH, False, True, True, False),
])
def test_config_class(require_checks, method, delete_branch, admin, auto, dry_run) -> None:
    cfg = Config(
        require_checks=require_checks,
        method=method,
        delete_branch=delete_branch,
        admin=admin,
        auto=auto,
        dry_run=dry_run,
        output_dir=Path("/tmp"),
    )
    assert cfg.require_checks == require_checks
    assert cfg.method == method
    assert cfg.delete_branch == delete_branch
