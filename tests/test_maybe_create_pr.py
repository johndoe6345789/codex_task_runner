import pytest
from unittest.mock import patch
from pathlib import Path
from codex_task_runner.pr.maybe_create_pr import _maybe_create_pr
from codex_task_runner.etc.task_ref import TaskRef
from codex_task_runner.etc.config_class import Config
from codex_task_runner.etc.merge_method import MergeMethod


@pytest.fixture
def cfg() -> Config:
    return Config(
        require_checks=True,
        method=MergeMethod.SQUASH,
        delete_branch=True,
        admin=False,
        auto=False,
        dry_run=False,
        output_dir=Path("/tmp"),
    )


def test_maybe_create_pr_no_branch(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    with patch("codex_task_runner.pr.maybe_create_pr.find_head_branch") as mock_find:
        mock_find.return_value = None
        result = _maybe_create_pr(cfg, t)
        assert result is None


def test_maybe_create_pr_existing(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    with patch("codex_task_runner.pr.maybe_create_pr.find_head_branch") as mock_find:
        with patch("codex_task_runner.pr.maybe_create_pr.pr_exists_open") as mock_exists:
            mock_find.return_value = "codex/title"
            mock_exists.return_value = 55
            result = _maybe_create_pr(cfg, t)
            assert result == 55


def test_maybe_create_pr_creates(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    with patch("codex_task_runner.pr.maybe_create_pr.find_head_branch") as mock_find:
        with patch("codex_task_runner.pr.maybe_create_pr.pr_exists_open") as mock_exists:
            with patch("codex_task_runner.pr.maybe_create_pr.create_pr") as mock_create:
                mock_find.return_value = "codex/title"
                mock_exists.return_value = None
                mock_create.return_value = 101
                result = _maybe_create_pr(cfg, t)
                assert result == 101
