import unittest
from codex_task_runner.textutil import slugify, words


class TestTextUtil(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(slugify("Add A, B, and C!"), "add-a-b-and-c")

    def test_words(self) -> None:
        self.assertEqual(words("Hello, World!"), ["hello", "world"])
