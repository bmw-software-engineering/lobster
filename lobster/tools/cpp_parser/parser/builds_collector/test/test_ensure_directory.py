import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.directory_utils import (
    ensure_directory,
)


class TestEnsureDirectory(TestCase):
    def setUp(self) -> None:
        self.test_dir = Path("test")

    def tearDown(self) -> None:
        pass

    @patch.object(Path, "is_dir", return_value=True)
    @patch.object(Path, "mkdir")
    def test_ensure_directory_exist(self, mock_mkdir: MagicMock, mock_is_dir: MagicMock) -> None:
        """
        Verify that when the directory already exists, ensure_directory does not call mkdir
        """
        ensure_directory(self.test_dir)
        mock_is_dir.assert_called_once()
        mock_mkdir.assert_not_called()

    @patch.object(Path, "is_dir", return_value=False)
    @patch.object(Path, "mkdir")
    def test_ensure_directory_not_exist(self, mock_mkdir: MagicMock, mock_is_dir: MagicMock) -> None:
        """
        Verify that when the directory does not exist, ensure_directory creates the directory
        """
        ensure_directory(self.test_dir)
        mock_is_dir.assert_called_once()
        mock_mkdir.assert_called_once()


if __name__ == "__main__":
    unittest.main()
