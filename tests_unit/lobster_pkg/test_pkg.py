import os
import json
import unittest
from tempfile import TemporaryDirectory
from os.path import dirname
from pathlib import Path
import xml.etree.ElementTree as ET

from lobster.common.exceptions import LOBSTER_Exception
from lobster.tools.pkg.pkg import (
    create_raw_entry,
    extract_lobster_traces_from_trace_analysis,
    xml_parser,
    create_default_activity,
)


class LobsterPkgTests(unittest.TestCase):
    # unit tests for lobster-pkg

    def setUp(self):

        self.test_fake_dir = str(Path(dirname(__file__), "not_existing"))
        self.test_data_dir = str(Path(dirname(__file__), "data"))
        self.test_pkg_file_1 = str(Path(dirname(__file__), "data", "sample1.pkg"))
        self.test_pkg_file_2 = str(Path(dirname(__file__), "data", "sample2.pkg"))
        self.test_pkg_file_with_misplaced = str(Path(dirname(__file__), "data", "sample_with_misplaced.pkg"))
        self.test_fake_file = str(Path(dirname(__file__), "data", "not_existing.pkg"))

        self.temp_dir = TemporaryDirectory() # pylint: disable=R1732

        self.output_pkg_file_1 = os.path.join(self.temp_dir.name, "sample1.lobster")
        self.output_pkg_file_2 = os.path.join(self.temp_dir.name, "sample2.lobster")

    def test_lobster_pkg_functions_with_valid_xml_format(self):
        data = {}
        expected_values = ["req banana.reqA", "req banana.reqB", "req valid.req1", "req valid.req2"]
        with open(self.test_pkg_file_1, "r", encoding="UTF-8") as file:
            filename = Path(self.test_pkg_file_1).name
            file_content = file.read()
            getvalues = xml_parser(file_content, filename)

            self.assertIsInstance(getvalues, list)
            self.assertEqual(1, len(getvalues))
            self.assertEqual("lobster-trace: banana.reqA,banana.reqB", getvalues[0].get('trace'))

            tree = ET.fromstring(file_content)
            valid_traces, misplaced_traces = extract_lobster_traces_from_trace_analysis(
                tree, filename
            )
            self.assertIsInstance(valid_traces, list)
            self.assertEqual(1, len(valid_traces))
            self.assertEqual("lobster-trace: valid.req1,valid.req2", valid_traces[0].get('trace'))

            self.assertIsInstance(misplaced_traces, list)
            self.assertEqual(1, len(misplaced_traces))
            self.assertIn("lobster-trace: misplaced.req1,misplaced.req2", misplaced_traces[0])

            getvalues.extend(valid_traces)
            create_raw_entry(data, file.name, json.dumps(getvalues))

        lobster_items = list(data.values())
        for item in lobster_items:
            lobster_item = item.to_json()
            self.assertTrue(lobster_item['refs'] == expected_values)

    def test_lobster_pkg_functions_with_misplaced_lobster_lines(self):
        with open(self.test_pkg_file_with_misplaced, "r", encoding="UTF-8") as file:
            filename = Path(self.test_pkg_file_with_misplaced).name
            file_content = file.read()

            with self.assertRaises(LOBSTER_Exception) as ctx:
                xml_parser(file_content, filename)
            exception_message = str(ctx.exception.message)
            self.assertIn("Misplaced LOBSTER tag(s)", exception_message)
            self.assertIn(filename, exception_message)
            self.assertIn("at line(s): [20]", exception_message)

    def test_lobster_pkg_functions_with_invalid_xml_format(self):
        data = {}
        with open(self.test_pkg_file_2, "r", encoding="UTF-8") as file:
            filename = Path(self.test_pkg_file_2).name
            file_content = file.read()
            getvalues = xml_parser(file_content, filename)

            self.assertIsInstance(getvalues, list)
            self.assertEqual(0, len(getvalues))

            tree = ET.fromstring(file_content)
            valid_traces, misplaced_traces = extract_lobster_traces_from_trace_analysis(
                tree, filename
            )
            self.assertIsInstance(valid_traces, list)
            self.assertEqual(0, len(valid_traces))

            self.assertIsInstance(misplaced_traces, list)
            self.assertEqual(0, len(misplaced_traces))

            create_default_activity(file_content, filename, data)

            self.assertIn('pkg sample2.pkg',list(data.keys()))
            lobster_items = list(data.values())
            for item in lobster_items:
                lobster_item = item.to_json()
                self.assertTrue(lobster_item['framework'] == "lobster-pkg")
                self.assertTrue(lobster_item['kind'] == "test")

    def tearDown(self):
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
