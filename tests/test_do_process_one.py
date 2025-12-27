import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from codex_task_runner.process.do_process_one import process_one
from codex_task_runner.etc.task_ref import TaskRef
from codex_task_runner.etc.config_class import Config
from codex_task_runner.etc.merge_method import MergeMethod
from codex_task_runner.etc.pull_request import PullRequest


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


def test_do_process_one_no_pr(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=())
    
    with patch("codex_task_runner.process.do_process_one.task_pr_number") as mock_prn:
        with patch("codex_task_runner.process.do_process_one.append_text"):
            mock_prn.return_value = None
            process_one(cfg, t)
            # Should return early with no PR


def test_do_process_one_with_pr(cfg: Config) -> None:
    t = TaskRef(task_id="t1", title="Title", repo="o/r", base_branch="main", pr_numbers=(42,))
    pr = PullRequest(number=42, url="http://gh/42", title="T", author="a", state="open", mergeable="MERGEABLE", checks_state="SUCCESS")
    
    with patch("codex_task_runner.process.do_process_one.task_pr_number") as mock_prn:
        with patch("codex_task_runner.process.do_process_one.get_pr") as mock_get:
            with patch("codex_task_runner.process.do_process_one.merge_pr") as mock_merge:
                with patch("codex_task_runner.process.do_process_one.append_text"):
                    mock_prn.return_value = 42
                    mock_get.return_value = pr
                    mock_merge.return_value = True
                    process_one(cfg, t)
