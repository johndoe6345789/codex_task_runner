import unittest
from codex_task_runner.codex.parse_tasks import parse_tasks


class TestParse(unittest.TestCase):
    def test_parse_minimal(self) -> None:
        obj = {"items": [{"id": "t1", "title": "X",
                          "task_status_display": {"environment_label": "o/r",
                                                 "branch_name": "main"},
                          "pull_requests": []}]}
        tasks = parse_tasks(obj)
        self.assertEqual(tasks[0].repo, "o/r")
        self.assertEqual(tasks[0].pr_numbers, ())
