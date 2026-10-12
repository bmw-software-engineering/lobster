import tempfile
import unittest

from yamale import YamaleError

from lobster.tools.trlc.lobster_trlc_config import LobsterTrlcConfig
from lobster.tools.trlc.instruction import InstructionType


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
        # lobster-trace: trlc_req.Lobster_Trlc_Config_Parses_Rules
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
                "  - package: another_package\n"
                "    record-type: another_type\n"
                "    namespace: imp\n"
                "    version-field: another_version\n"
                "    description-fields: [title, summary]\n"
                "    justification-up-fields: [up_a, up_b]\n"
                "    justification-down-fields: [down]\n"
                "    justification-global-fields: [global]\n"
                "    tags:\n"
                "      - field: tag_value\n"
                "        namespace: custom\n"
                "    applies-to-derived-types: false\n"
                "to-string-rules:\n"
                "  - package: my_package\n"
                "    tuple-type: MyTuple\n"
                "    to-string:\n"
                "      - 'prefix $(name)'\n"
                "  - package: another_package\n"
                "    tuple-type: AnotherTuple\n"
                "    to-string:\n"
                "      - '$(id)-suffix'\n"
            )
            file_name = fd.name

        config = LobsterTrlcConfig.from_file(file_name)
        self.assertEqual(len(config.conversion_rules), 2)
        rule = config.conversion_rules[0]
        self.assertEqual(rule.package_name, "my_package")
        self.assertEqual(rule.type_name, "my_type")
        self.assertEqual(rule.version, "my_version")
        self.assertEqual(rule.description_fields, ["description"])
        self.assertTrue(rule.applies_to_derived_types)
        another_rule = config.conversion_rules[1]
        self.assertEqual(another_rule.package_name, "another_package")
        self.assertEqual(another_rule.type_name, "another_type")
        self.assertEqual(another_rule.lobster_namespace, "imp")
        self.assertEqual(another_rule.version, "another_version")
        self.assertEqual(another_rule.description_fields, ["title", "summary"])
        self.assertEqual(another_rule.justification_up_fields, ["up_a", "up_b"])
        self.assertEqual(another_rule.justification_down_fields, ["down"])
        self.assertEqual(another_rule.justification_global_fields, ["global"])
        self.assertEqual(another_rule.tags[0].field, "tag_value")
        self.assertEqual(another_rule.tags[0].namespace, "custom")
        self.assertFalse(another_rule.applies_to_derived_types)
        self.assertEqual(len(config.to_string_rules), 2)
        to_string_rule = config.to_string_rules[0]
        self.assertEqual(to_string_rule.package_name, "my_package")
        self.assertEqual(to_string_rule.tuple_type_name, "MyTuple")
        self.assertEqual(len(to_string_rule.rules), 1)
        self.assertEqual(
            [(instruction.typ, instruction.value)
             for instruction in to_string_rule.rules[0]],
            [
                (InstructionType.CONSTANT_TEXT, "prefix "),
                (InstructionType.FIELD, "name"),
            ],
        )
        another_to_string_rule = config.to_string_rules[1]
        self.assertEqual(another_to_string_rule.package_name, "another_package")
        self.assertEqual(another_to_string_rule.tuple_type_name, "AnotherTuple")
        self.assertEqual(len(another_to_string_rule.rules), 1)
        self.assertEqual(
            [(instruction.typ, instruction.value)
             for instruction in another_to_string_rule.rules[0]],
            [(InstructionType.FIELD, "id"), (InstructionType.CONSTANT_TEXT, "-suffix")],
        )

    def test_from_dict_defaults(self):
        # lobster-trace: trlc_req.Lobster_Trlc_Config_Parses_Rules
        config = LobsterTrlcConfig.from_dict({})
        self.assertEqual(config.conversion_rules, [])
        self.assertEqual(config.to_string_rules, [])
        self.assertEqual(config.extensions, (".rsl", ".trlc", ".trlc.md"))


if __name__ == "__main__":
    unittest.main()
