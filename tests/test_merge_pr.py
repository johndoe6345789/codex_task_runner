import pytest
from unittest.mock import patch
from codex_task_runner.gh.merge_pr import merge_pr
from codex_task_runner.etc.merge_method import MergeMethod
from codex_task_runner.proc.proc_result import ProcResult


def test_merge_pr_dry_run() -> None:
    result = merge_pr("owner/repo", 1, MergeMethod.SQUASH, delete_branch=True, admin=False, auto=False, dry_run=True)
    assert result is True


def test_merge_pr_success() -> None:
    with patch("codex_task_runner.gh.merge_pr.run") as mock_run:
        mock_run.return_value = ProcResult(code=0, out="Merged", err="")
        result = merge_pr("owner/repo", 1, MergeMethod.SQUASH, delete_branch=True, admin=False, auto=False, dry_run=False)
        assert result is True


def test_merge_pr_failure() -> None:
    with patch("codex_task_runner.gh.merge_pr.run") as mock_run:
        mock_run.return_value = ProcResult(code=1, out="", err="error")
        result = merge_pr("owner/repo", 1, MergeMethod.MERGE, delete_branch=False, admin=False, auto=False, dry_run=False)
        assert result is False
