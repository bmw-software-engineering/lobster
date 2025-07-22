import pathlib
import unittest
from pathlib import Path
import subprocess

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

    def test_commit_hash_for_main_repo(self):
        root = "abc"
        submodule_roots = {}
        repo_root = pathlib.Path().cwd()
        git_hash_cache = {}
        location = File_Reference("123.def")
        tag = Tracing_Tag("test_namespace", "ÄÖÜ")
        item = Item(tag, location)
        expected_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            universal_newlines=True,
            cwd=Path(__file__).parent,
        ).strip()
        _, _, commit = get_git_commit_hash_repo_and_path(
            root, submodule_roots, item, repo_root, git_hash_cache)
        self.assertEqual(expected_commit, commit)

if __name__ == '__main__':
    unittest.main()
