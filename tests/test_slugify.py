import unittest
from codex_task_runner.etc.slugify import slugify
from codex_task_runner.etc.words import words


class TestTextUtil(unittest.TestCase):
    def test_slugify(self) -> None:
        self.assertEqual(slugify("Add A, B, and C!"), "add-a-b-and-c")

    def test_words(self) -> None:
        self.assertEqual(words("Hello, World!"), ["hello", "world"])
