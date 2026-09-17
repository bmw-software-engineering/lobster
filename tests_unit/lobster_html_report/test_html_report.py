# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2024-2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

import unittest
import hashlib
import subprocess
from datetime import datetime, timezone
from unittest.mock import patch
from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc, name_hash


class LobsterHtmlReportTests(unittest.TestCase):
    def test_timestamp_found_in_main_repo(self):
        """Test when commit is found in main repo"""
        head_commit = "HEAD"
        result = subprocess.run(
            ['git', 'show', '-s', '--format=%ct', head_commit],
            capture_output=True, text=True, check=True
        )
        epoch_time = int(result.stdout.strip())
        expected_time = datetime.fromtimestamp(epoch_time, tz=timezone.utc)

        returned = get_commit_timestamp_utc(head_commit)
        self.assertIn(str(expected_time), returned)
        self.assertNotIn("from submodule", returned)

    def test_timestamp_unknown_commit(self):
        """Test when commit is not found in repo or submodules"""
        invalid_commit = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        returned = get_commit_timestamp_utc(invalid_commit)
        self.assertEqual(returned, "Unknown")

    def test_timestamp_found_in_submodule(self):
        """Test when commit is found only in submodule"""
        with patch("lobster.tools.core.html_report.html_report.run_git_show") as mock_run:
            # First call (main repo) returns None, second call (submodule) returns timestamp
            mock_run.side_effect = [None, "2026-06-25T12:00:00Z"]
            returned = get_commit_timestamp_utc("abc123", submodule_path="submodule/path")
            self.assertEqual(returned, "2026-06-25T12:00:00Z (from submodule at submodule/path)")

    def test_name_hash_returns_expected_md5_hash(self):
        """Ensure name_hash matches hashlib.md5 for multiple inputs"""
        test_cases = [
            ("", hashlib.md5("".encode("UTF-8")).hexdigest()),          # empty string
            ("Unit", hashlib.md5("Unit".encode("UTF-8")).hexdigest()),  # ASCII
            ("Straße", hashlib.md5("Straße".encode("UTF-8")).hexdigest()),  # Special Character
            ("Test", hashlib.md5("Test".encode("UTF-8")).hexdigest()),  # consistency check
        ]

        for input_str, expected in test_cases:
            with self.subTest(name=input_str):
                self.assertEqual(name_hash(input_str), expected)

    def test_name_hash_returns_different_hashes_for_different_inputs(self):
        """Different inputs should yield different hashes"""
        self.assertNotEqual(name_hash("Unit"), name_hash("Test"))


if __name__ == "__main__":
    unittest.main()
