import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from codex_task_runner.process.process_tasks import process_tasks
from codex_task_runner.etc.task_ref import TaskRef
from codex_task_runner.etc.config_class import Config
from codex_task_runner.etc.merge_method import MergeMethod


@pytest.fixture
def cfg(tmp_path: Path) -> Config:
    return Config(
        require_checks=True,
        method=MergeMethod.SQUASH,
        delete_branch=True,
        admin=False,
        auto=False,
        dry_run=True,
        output_dir=tmp_path,
    )


def test_process_tasks_empty(cfg: Config) -> None:
    with patch("codex_task_runner.process.process_tasks.process_one") as mock_one:
        process_tasks(cfg, [])
        mock_one.assert_not_called()


def test_process_tasks_with_tasks(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    
    with patch("codex_task_runner.process.process_tasks.process_one") as mock_one:
        process_tasks(cfg, [t])
        mock_one.assert_called_once()
