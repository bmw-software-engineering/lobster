import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from os.path import dirname
from pathlib import Path

from lobster.tools.core.online_report.online_report import main


class LobsterOnlineReportTests(unittest.TestCase):
    def setUp(self):
        self.input_file = str(Path(dirname(__file__), "data",
                                   "report-lobster.output"))
        self.online_report = "online-report.lobster"

    def test_valid_inputs(self):
        sys.argv = ["lobster-online-report", self.input_file,
                    f'--out={self.online_report}']
        with StringIO() as stdout, redirect_stdout(stdout):
            exit_code = main()
            output = stdout.getvalue()
        with open(self.online_report, 'r') as file:
            data = json.load(file)
            for level in data['levels']:
                for item in level['items']:
                    with self.subTest(item):
                        location = item['location']
                        if 'file' in location:
                            self.assertIsNotNone(location.get('commit'))
        self.assertEqual(exit_code, 0)
        self.assertIn(f"LOBSTER report {self.online_report} "
                      f"changed to use online references", output)


if __name__ == '__main__':
    unittest.main()
