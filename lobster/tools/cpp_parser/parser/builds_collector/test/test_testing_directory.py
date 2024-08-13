import unittest
from unittest import TestCase

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.directory_utils import (
    TestDirectory,
)


class TestTestDirectory(TestCase):
    def setUp(self) -> None:
        self.test_dir_object = TestDirectory()
        self.test_dir = self.test_dir_object.get_directory()

    def tearDown(self) -> None:
        self.test_dir_object.clear_directory()

    def test_test_directory_exist(self) -> None:
        self.assertTrue((self.test_dir).is_dir())

    def test_test_directory_clear(self) -> None:
        self.test_dir_object.clear_directory()
        self.assertFalse((self.test_dir).is_dir())


if __name__ == "__main__":
    unittest.main()
