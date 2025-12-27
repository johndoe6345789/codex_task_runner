import pytest
import tempfile
from codex_task_runner.etc.make_config import make_config
from codex_task_runner.etc.merge_method import MergeMethod


@pytest.mark.parametrize("method,keep_branch,dry_run", [
    ("merge", False, True),
    ("squash", True, False),
    ("rebase", False, False),
])
def test_make_config(method, keep_branch, dry_run) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = make_config(
            require_checks=True,
            method=method,
            keep_branch=keep_branch,
            admin=False,
            auto=False,
            dry_run=dry_run,
            output_dir=tmpdir,
        )
        assert cfg.method == MergeMethod(method)
        assert cfg.delete_branch == (not keep_branch)
        assert cfg.dry_run == dry_run
