import unittest
from pathlib import Path
from unittest.mock import patch
from os.path import dirname

from lobster.common.report import Report
from lobster.common.location import Github_Reference
from lobster.tools.core.online_report.online_report import (
    load_config,
    add_github_reference_to_items,
    Config
)


class LobsterOnlineReportTests(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = str(Path(dirname(__file__), "data"))
        self.test_config_1 = str(Path(dirname(__file__), "data", "online-report-config.yaml"))
        self.repo_url = 'https://github.com/test-repo'
        self.config_data = Config(
            repo_root=self.repo_url,
            base_url='/something',
            commit_id='abc123def456',
            report=self.test_data_dir + '/report.lobster'
        )

    def test_load_config(self):
        config = load_config(self.test_config_1)
        self.assertEqual(config.repo_root, "https://github.com/test-repo")
        self.assertEqual(config.base_url, "/something")
        self.assertEqual(config.commit_id, "abc123def456")
        self.assertEqual(config.report, "report.lobster")

    @patch('lobster.tools.core.online_report.online_report.PathToUrlConverter')
    def test_add_github_reference_to_items(self, mock_converter_class):
        # Set up mock converter
        mock_converter = mock_converter_class.return_value
        mock_converter.path_to_url.return_value = type('UrlParts', (), {
            'url_start': 'https://github.com/bmw-software-engineering/lobster',
            'commit_hash': 'abc123def456',
            'path_html': 'test-lobster-online-report/basic.py'
        })
        report = Report()
        report.load_report(self.config_data.report)
        add_github_reference_to_items(self.config_data.repo_root, self.config_data.base_url,
                                      report, self.config_data.commit_id)

        expected_locations ={
            "python basic.trlc_reference": {
                "location": {
                    "kind": "github",
                    "gh_root": "https://github.com/bmw-software-engineering/lobster",
                    "commit": "abc123def456",
                    "file": "test-lobster-online-report/basic.py",
                    "line": 5
                }
            },
            "python basic.Example.helper_function":{
                "location": {
                    "kind": "github",
                    "gh_root": "https://github.com/bmw-software-engineering/lobster",
                    "commit": "abc123def456",
                    "file": "test-lobster-online-report/basic.py",
                    "line": 13
                }
            },
                "python basic.Example.nor": {
                "location": {
                    "kind": "github",
                "gh_root": "https://github.com/bmw-software-engineering/lobster",
                    "commit": "abc123def456",
                    "file": "test-lobster-online-report/basic.py",
                    "line": 17
                }
            }
        }

        item_ids = list(report.items.keys())

        for item_id in item_ids:
            item = report.items[item_id]
            self.assertIsInstance(item.location, Github_Reference)
            self.assertEqual(item.location.gh_root, expected_locations[item_id]['location']['gh_root'])
            self.assertEqual(item.location.filename, expected_locations[item_id]['location']['file'])
            self.assertEqual(item.location.line, expected_locations[item_id]['location']['line'])
            self.assertEqual(item.location.commit, expected_locations[item_id]['location']['commit'])


if __name__ == '__main__':
    unittest.main()
