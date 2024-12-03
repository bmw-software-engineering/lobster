import unittest
import tempfile
import os
import sys
import yaml
import argparse
from contextlib import redirect_stdout
from io import StringIO
from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.location import Codebeamer_Reference
from lobster.errors import LOBSTER_Error
from lobster.tools.codebeamer.codebeamer import _create_common_params, _create_lobster_item, main, parse_yaml_config, ap

class TestCreateFunctions(unittest.TestCase):
    def setUp(self):
         # Create temporary directory and files for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'codebeamer-config.yaml')
        self.root_url = 'http://root_url'
        self.cb_item_template = {
            'version': 1,
            'tracker': {'id': 123}
        }

    def generate_cb_item(self, item_id, name):
        """Generate a codebeamer item dictionary."""

        return {
            'id': item_id,
            **self.cb_item_template,
            'name': name
        }

    def generate_common_params(self, namespace, item_name, kind, expected_class):
        """Generate a test case for common params and lobster item creation."""
        cb_item = self.generate_cb_item(1, item_name) 
        common_params = _create_common_params(namespace, cb_item, self.root_url, item_name, kind)

        return {
            'common_params': common_params,
            'item_name': item_name,
            'expected_class': expected_class,
            'tag': Tracing_Tag(namespace, str(cb_item["id"]), cb_item["version"]),
            'location': Codebeamer_Reference(self.root_url, cb_item["tracker"]["id"], cb_item["id"], cb_item["version"], item_name),
            'kind' : kind
        }

    def  generate_test_case(self):

        return [
            self.generate_common_params('req', 'Requirement Item', 'requirement', Requirement),
            self.generate_common_params('imp', 'Implementation Item', 'implementation', Implementation),
            self.generate_common_params('act', 'Activity Item', 'activity', Activity),
            ]

    def test_create_common_params(self):
        test_cases = self.generate_test_case()

        for case in test_cases:
            with self.subTest(case=case):
                self.assertEqual(case['common_params']['tag'].namespace, case['tag'].namespace)
                self.assertEqual(case['common_params']['tag'].tag, case['tag'].tag)
                self.assertEqual(case['common_params']['tag'].version, case['tag'].version)
                self.assertEqual(case['common_params']['location'].cb_root, case['location'].cb_root)
                self.assertEqual(case['common_params']['location'].tracker, case['location'].tracker)
                self.assertEqual(case['common_params']['location'].item, case['location'].item)
                self.assertEqual(case['common_params']['location'].version, case['location'].version)
                self.assertEqual(case['common_params']['location'].name, case['location'].name)
                self.assertEqual(case['common_params']['kind'], case['kind'])

    def test_create_lobster_item(self):
        # lobster-trace: codebeamer_req.Dummy_Requirement_Unit_Test
        test_cases = self.generate_test_case()

        for case in test_cases:
            with self.subTest(case=case):
                lobster_item = _create_lobster_item(case['expected_class'], case['common_params'], case['item_name'], None)
                self.assertIsInstance(lobster_item, case['expected_class'])
                self.assertEqual(lobster_item.tag, case['common_params']['tag'])
                self.assertEqual(lobster_item.location, case['common_params']['location'])
                self.assertEqual(lobster_item.kind, case['kind'])

                if case['kind'] == 'requirement':
                    self.assertEqual(lobster_item.framework, 'codebeamer')
                elif case['kind'] == 'implementation':
                    self.assertEqual(lobster_item.language, 'python')
                elif case['kind'] == 'activity':
                    self.assertEqual(lobster_item.framework, 'codebeamer')

    def tearDown(self):
        """
        This method is called after every test case.
        We use it to clean up resources like removing temporary files.
        """
        # Remove the temporary file created in setUp after the test completes
        self.temp_dir.cleanup()

    def reset_all_parsers(self):
        """Reset all existing argparse.ArgumentParser instances."""
        for obj in globals().values():
            if isinstance(obj, argparse.ArgumentParser):
                obj._actions.clear()
                obj._option_string_actions.clear()
                obj._defaults.clear()
                obj._subparsers = None

    def test_main_missing_yaml_file(self):
        """
        Test the main function with a non-existent YAML file.
        This checks if the main function raises a FileNotFoundError when the file is missing.
        """
        missing_config_path = os.path.join(self.temp_dir.name, 'missing-config.yaml')
        self.reset_all_parsers()

        sys.argv = ['codebeamer.py', '--config', missing_config_path]
        with StringIO() as stdout, redirect_stdout(stdout):
            exit_code = main()
            output = stdout.getvalue()

        self.assertEqual(exit_code, 1)
        self.assertIn(f"Config file '{missing_config_path}' not found", output)

    def test_main_missing_config_field(self):
        missing_field_yaml_path = os.path.join(self.temp_dir.name, 'missing-field.yaml')
        with open(missing_field_yaml_path, 'w', encoding='utf-8') as yaml_file:
            yaml_file.write("""
                            root: https://example.com
                            schema: Requirement
                            """)
        self.reset_all_parsers()

        sys.argv = ['codebeamer.py', '--config', missing_field_yaml_path]
        with self.assertRaises(KeyError) as context:
            main()

        self.assertIn('One of the required fields must be present:', str(context.exception))

    def test_unsupported_config_keys(self):
        # Create a YAML file with unsupported keys
        unsupported_config = {
            "unsupported_key": "value",
            "out": "trlc-config.conf",
            "import_query":8805855
        }
        unsupported_config_path = os.path.join(self.temp_dir.name, "unsupported_config.yaml")
        with open(unsupported_config_path, "w", encoding="utf-8") as f:
            yaml.dump(unsupported_config, f)

        self.reset_all_parsers()

        sys.argv = ["codebeamer.py", "--config", unsupported_config_path]

        # Capture stdout
        with self.assertRaises(KeyError) as context:
            main()

        self.assertIn("Unsupported config keys", str(context.exception))

# This block ensures that the tests are run when the script is executed directly
if __name__ == "__main__":
    unittest.main()
