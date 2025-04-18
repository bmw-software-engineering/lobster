import unittest
import subprocess
from datetime import datetime, timezone
from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc


class LobsterHtmlReportTests(unittest.TestCase):
    def test_timestamp_found_in_main_repo(self):
        """Test when commit is found in main repo"""
        self.head_commit = "HEAD"
        result = subprocess.run(
            ['git', 'show', '-s', '--format=%ct', self.head_commit],
            capture_output=True, text=True, check=True
        )
        epoch_time = int(result.stdout.strip())
        expected_time = datetime.fromtimestamp(epoch_time, tz=timezone.utc)

        returned = get_commit_timestamp_utc(self.head_commit)
        self.assertIn(str(expected_time), returned)
        self.assertNotIn("from submodule", returned)

    def test_timestamp_unknown_commit(self):
        """Test when commit is not found in repo or submodules"""
        self.invalid_commit = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        returned = get_commit_timestamp_utc(self.invalid_commit)
        self.assertEqual(returned, "Unknown")


if __name__ == "__main__":
    unittest.main()
