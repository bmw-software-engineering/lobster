import unittest
from pathlib import Path
from unittest.mock import patch

from lobster.items import Item, Tracing_Tag
from lobster.location import File_Reference
from lobster.tools.core.online_report.online_report import (
    get_summary, get_git_commit_hash_repo_and_path
)


class LobsterOnlineReportTests(unittest.TestCase):
    def test_print_summary_same_values(self):
        value = "marble"
        actual = get_summary(value, value)
        self.assertEqual(
            actual,
            f"LOBSTER report {value} modified to use online references.",
        )

    def test_print_summary_different_values(self):
        in_file = "basalt"
        out_file = "granite"
        actual = get_summary(in_file, out_file)
        self.assertEqual(
            actual,
            f"LOBSTER report {out_file} created, using online references.",
        )

    @patch('lobster.tools.core.online_report.online_report.get_hash_for_git_commit')
    def test_commit_hash_for_main_repo(self, mock_get_hash):
        mock_get_hash.return_value = "mocked_commit_hash"
        item = Item(
            Tracing_Tag("test_namespace", "ÄÖÜ"),
            File_Reference("123.def"),
        )
        _, _, commit = get_git_commit_hash_repo_and_path(
            gh_root="abc",
            gh_submodule_roots={},
            item=item,
            repo_root=Path(__file__).parent,
            git_hash_cache={},
        )
        self.assertEqual("mocked_commit_hash", commit)

if __name__ == '__main__':
    unittest.main()
