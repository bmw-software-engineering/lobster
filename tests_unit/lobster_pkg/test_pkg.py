import os
import json
import unittest
from tempfile import TemporaryDirectory
from os.path import dirname
from pathlib import Path
import xml.etree.ElementTree as ET
from types import SimpleNamespace

from lobster.tools.pkg.pkg import (
    create_raw_entry,
    extract_lobster_traces_from_trace_analysis,
    get_valid_files,
    write_to_file,
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
        self.test_fake_file = str(Path(dirname(__file__), "data", "not_existing.pkg"))

        self.temp_dir = TemporaryDirectory() # pylint: disable=R1732

        self.output_pkg_file_1 = os.path.join(self.temp_dir.name, "sample1.lobster")
        self.output_pkg_file_2 = os.path.join(self.temp_dir.name, "sample2.lobster")

    def test_get_valid_files(self):
        test_cases = [
            {
                "input": [self.test_pkg_file_1],
                "expected_length": 1,
                "case": "one_pkg_file",
            },
            {
                "input": [self.test_pkg_file_1, self.test_pkg_file_2],
                "expected_length": 2,
                "case": "two_pkg_files",
            },
            {
                "input": [self.test_data_dir],
                "expected_length": 2,
                "case": "valid_dir",
            },
            {
                "input": [self.test_fake_dir],
                "expected_length": 0,
                "case": "invalid_dir",
                "error": True
            },
             {
                "input": [self.test_fake_dir],
                "expected_length": 0,
                "case": "invalid_dir",
                "error": True
            },
             {
                "input": [self.test_fake_file],
                "expected_length": 0,
                "case": "invalid_file",
                "error": True
            },
        ]

        for test_case in test_cases:
            with self.subTest(i=test_case["case"]):
                if test_case.get("error"):
                    with self.assertRaises(FileNotFoundError):
                        get_valid_files(test_case["input"])
                else:
                    file_list = get_valid_files(test_case["input"])
                    self.assertIsInstance(file_list, list)
                    self.assertEqual(test_case["expected_length"], len(file_list))

    def test_lobster_pkg_functions_with_valid_xml_format(self):
        data = {}
        options = SimpleNamespace(out=self.output_pkg_file_1)
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

            write_to_file(options, data)

        with open(self.output_pkg_file_1, "r", encoding="UTF-8") as lobster_file:
            file_content = lobster_file.read()
            for excpected_value in expected_values:
                self.assertIn(excpected_value, file_content)

    def test_lobster_pkg_functions_with_invalid_xml_format(self):
        data = {}
        options = SimpleNamespace(out=self.output_pkg_file_2)

        expected_values = ['"schema": "lobster-act-trace"', '"generator": "lobster-pkg"']

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

            write_to_file(options, data)

            with open(self.output_pkg_file_2, "r", encoding="UTF-8") as lobster_file:
                file_content = lobster_file.read()
                for excpected_value in expected_values:
                    self.assertIn(excpected_value, file_content)


    def tearDown(self):
        self.temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()
