import unittest
from pathlib import Path

from lobster.report import Report


class CoreTest(unittest.TestCase):

    def setUp(self):
        self.lobster_config1 = str(Path('./data', 'lobster1.config'))

    def test_lobster_report_parse_config(self):
        report = Report()

        report.parse_config(self.lobster_config1)

        self.assertEqual(8, len(report.config))
        self.assertEqual(8, len(report.coverage))
        self.assertEqual(6, len(report.items))

        expect = {'Laws': {'items': 1, 'ok': 1, 'coverage': 100.0},
                  'System Requirements': {'items': 2, 'ok': 1, 'coverage': 50.0},
                  'Software Requirements': {'items': 1, 'ok': 0, 'coverage': 0.0},
                  'Implementation': {'items': 1, 'ok': 0, 'coverage': 0.0},
                  'Unit Test': {'items': 0, 'ok': 0, 'coverage': 100.0},
                  'Component Test': {'items': 0, 'ok': 0, 'coverage': 100.0},
                  'Empty': {'coverage': 100.0, 'items': 0, 'ok': 0},
                  'Another Test': {'coverage': 0.0, 'items': 1, 'ok': 0}}
        self.assertEqual(expect, report.coverage)


if __name__ == '__main__':
    unittest.main()
