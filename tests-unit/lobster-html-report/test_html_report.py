import unittest
import subprocess
from datetime import datetime, timezone
from lobster.tools.core.html_report.html_report import get_commit_timestamp_utc


class LobsterHtmlReportTests(unittest.TestCase):
    def setUp(self):
        self.valid_commit_hash = "HEAD"
        self.invalid_commit_hash = "invalidhash"

    def test_get_commit_timestamp_utc_valid_commit(self):
        # Ensure a valid commit hash from the report
        if not self.valid_commit_hash:
            self.skipTest("No valid commit hash provided from the report")

        result = subprocess.run(
            ['git', 'show', '-s', '--format=%ct', self.valid_commit_hash],
            capture_output=True, text=True, check=True
        )

        epoch_time = int(result.stdout.strip())
        expected_utc_time = datetime.fromtimestamp(epoch_time, tz=timezone.utc)

        self.assertEqual(get_commit_timestamp_utc(self.valid_commit_hash), expected_utc_time)

    def test_get_commit_timestamp_utc_invalid_commit(self):
        self.assertIsNone(get_commit_timestamp_utc(self.invalid_commit_hash))


if __name__ == "__main__":
    unittest.main()
