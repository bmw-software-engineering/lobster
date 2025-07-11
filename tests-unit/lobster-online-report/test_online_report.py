import json
import pathlib
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from os.path import dirname
from pathlib import Path
import subprocess

from lobster.items import Item, Tracing_Tag
from lobster.location import File_Reference
from lobster.tools.core.online_report.online_report import (
    main, get_summary, get_git_commit_hash_repo_and_path
)


class LobsterOnlineReportTests(unittest.TestCase):
    def test_valid_inputs(self):
        input_file = str(Path(dirname(__file__), "data",
                                   "report-lobster.output"))
        online_report = "online-report.lobster"

        sys.argv = ["lobster-online-report", input_file,
                    f'--out={online_report}']
        with StringIO() as stdout, redirect_stdout(stdout):
            exit_code = main()
        with open(online_report, 'r', encoding="UTF-8") as file:
            data = json.load(file)
            for level in data['levels']:
                for item in level['items']:
                    with self.subTest(item):
                        location = item['location']
                        if 'file' in location:
                            self.assertIsNotNone(location.get('commit'))
        self.assertEqual(exit_code, 0)

    def test_print_summary_same_values(self):
        value = "marble"
        actual = get_summary(value, value)
        self.assertEqual(actual, f"LOBSTER report {value} modified to use online references.")

    def test_print_summary_different_values(self):
        in_file = "basalt"
        out_file = "granite"
        actual = get_summary(in_file, out_file)
        self.assertEqual(actual, f"LOBSTER report {out_file} created, using online references.")

    def test_commit_hash_for_main_repo(self):
        root = " https://github.com/bmw-software-engineering/lobster"
        submodule_roots = {}
        repo_root = pathlib.Path().cwd()
        git_hash_cache = {}
        location = File_Reference("/data/basic.py")
        tag = Tracing_Tag("test_namespace", "python basic.trlc_reference")
        item = Item(tag, location)
        expected_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            universal_newlines=True, cwd=repo_root
        ).strip()
        _, _, commit = get_git_commit_hash_repo_and_path(
            root, submodule_roots, item, repo_root, git_hash_cache)
        self.assertEqual(expected_commit, commit)

if __name__ == '__main__':
    unittest.main()
