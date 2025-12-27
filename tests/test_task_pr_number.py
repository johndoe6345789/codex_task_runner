import pytest
from unittest.mock import patch
from pathlib import Path
from codex_task_runner.pr.task_pr_number import task_pr_number
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


def test_task_pr_number_existing(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=(42,))
    with patch("codex_task_runner.pr.task_pr_number._first_open") as mock_first:
        mock_first.return_value = 42
        result = task_pr_number(cfg, t)
        assert result == 42


def test_task_pr_number_create(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    with patch("codex_task_runner.pr.task_pr_number._first_open") as mock_first:
        with patch("codex_task_runner.pr.task_pr_number._maybe_create_pr") as mock_create:
            mock_first.return_value = None
            mock_create.return_value = 99
            result = task_pr_number(cfg, t)
            assert result == 99
