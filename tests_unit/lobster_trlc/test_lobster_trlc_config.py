import tempfile
import unittest

from yamale import YamaleError

from lobster.tools.trlc.lobster_trlc_config import LobsterTrlcConfig


class LobsterTrlcConfigTest(unittest.TestCase):
    def test_from_file_missing_file_raises(self):
        # lobster-trace: trlc_req.Lobster_Trlc_Config_From_File_Missing_Raises
        with self.assertRaises(FileNotFoundError):
            LobsterTrlcConfig.from_file("/no/such/config.yaml")

    def test_from_file_invalid_schema_raises(self):
        # lobster-trace: trlc_req.Lobster_Trlc_Config_From_File_Invalid_Schema_Raises
        with tempfile.NamedTemporaryFile(
                "w", suffix=".yaml", delete=False) as fd:
            fd.write("inputs: []\n")
            file_name = fd.name

        with self.assertRaises(YamaleError) as ctx:
            LobsterTrlcConfig.from_file(file_name)
        self.assertIn("conversion-rules", str(ctx.exception))

    def test_from_file_valid_config(self):
        # lobster-trace: trlc_req.Lobster_Trlc_Config_From_File_Parses_Conversion_Rules
        with tempfile.NamedTemporaryFile(
                "w", suffix=".yaml", delete=False) as fd:
            fd.write(
                "conversion-rules:\n"
                "  - package: my_package\n"
                "    record-type: my_type\n"
                "    namespace: req\n"
                "    version-field: my_version\n"
                "    description-fields: [description]\n"
                "    applies-to-derived-types: true\n"
            )
            file_name = fd.name

        config = LobsterTrlcConfig.from_file(file_name)
        self.assertEqual(len(config.conversion_rules), 1)
        rule = config.conversion_rules[0]
        self.assertEqual(rule.package_name, "my_package")
        self.assertEqual(rule.type_name, "my_type")
        self.assertEqual(rule.version, "my_version")
        self.assertEqual(rule.description_fields, ["description"])
        self.assertTrue(rule.applies_to_derived_types)
        self.assertEqual(config.to_string_rules, [])

    def test_from_dict_defaults(self):
        # lobster-trace: trlc_req.Lobster_Trlc_Config_From_File_Parses_Conversion_Rules
        config = LobsterTrlcConfig.from_dict({})
        self.assertEqual(config.conversion_rules, [])
        self.assertEqual(config.to_string_rules, [])
        self.assertEqual(config.extensions, (".rsl", ".trlc", ".trlc.md"))


if __name__ == "__main__":
    unittest.main()
