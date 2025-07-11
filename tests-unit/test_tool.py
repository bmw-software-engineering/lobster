import unittest
import os
import argparse
from tempfile import NamedTemporaryFile, TemporaryDirectory
import yaml

from lobster.errors import Message_Handler
from lobster.tool import LOBSTER_Tool

class ConcreteLOBSTER_Tool(LOBSTER_Tool):
    def __init__(self, name, description, extensions, official=False):
        super().__init__(name, description, extensions, official)

    def process_tool_options(self, options, work_list):
        pass

    def _run_impl(self, options: argparse.Namespace) -> int:
        return 0


class TestLOBSTER_Tool(unittest.TestCase):

    def setUp(self):
        self.tool = ConcreteLOBSTER_Tool("test", "Test description", ["lobster"], True)

    def test_init(self):
        self.assertEqual(self.tool.name, "lobster-test")
        self.assertEqual(self.tool.extensions, [".lobster"])
        self.assertIsInstance(self.tool.mh, Message_Handler)

    def test_load_yaml_config_valid_file(self):
        with NamedTemporaryFile("w", delete=False) as temp:
            yaml.dump({"elephant": "value"}, temp)
            temp_path = temp.name

        try:
            config = self.tool.load_yaml_config(temp_path)
            self.assertEqual(config, {"elephant": "value"})
        finally:
            os.remove(temp_path)

    def test_load_yaml_config_missing_file(self):
        with self.assertRaises(SystemExit) as context:
            self.tool.load_yaml_config("non_existent.yaml")
        self.assertEqual(str(context.exception), "Error: Config file 'non_existent.yaml' not found.")

    def test_process_common_options_output_exits_not_file(self):
        with TemporaryDirectory() as temp_dir:
            options = argparse.Namespace(out=temp_dir, inputs=[], inputs_from_file=None)
            with self.assertRaises(SystemExit):
                self.tool.process_common_options(options)

    def test_process_common_options_valid_inputs(self):
        with TemporaryDirectory():
            with  NamedTemporaryFile("w", delete=False) as temp:
                temp_path = temp.name

        options = argparse.Namespace(out=None, inputs=[temp_path], inputs_from_file=None)
        work_list = self.tool.process_common_options(options)
        self.assertEqual(work_list, [temp_path])

    def test_process_common_options_invalid_inputs(self):
        options = argparse.Namespace(out=None, inputs=["invalid.txt"], inputs_from_file=None)
        with self.assertRaises(SystemExit):
            self.tool.process_common_options(options)

if __name__ == "__main__":
    unittest.main()
