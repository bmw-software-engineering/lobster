import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_trlc.lobster_system_test_case_base import \
    LobsterTrlcSystemTestCaseBase


class ConversionRuleErrorTest(LobsterTrlcSystemTestCaseBase):
    def test_field_does_not_exist(self):
        """Test that an error is raised when field does not exist in the record type."""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated.lobster"
        rules = {
            "package": "extraction_test",
            "record-type": "base_type",
            "namespace": "req",
            "description-fields": ["does_not_exist_field"],
        }
        test_runner.config_file_data.conversion_rules = [rules]
        test_runner.declare_input_file(self._data_directory /
                                        "extraction_hierarchy.trlc")
        test_runner.declare_input_file(self._data_directory /
                                        "extraction_hierarchy.rsl")

        completed_process = test_runner.run_tool_test()
        print(completed_process.stderr)
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertStdErrText(
            "lobster-trlc: Invalid conversion rule defined in config.yaml: "
            "Component 'does_not_exist_field' not found in TRLC Record_Object "
            "'extraction_test.A'!\n"
        )
        asserter.assertExitCode(1)

    def test_field_does_not_exist_no_schema(self):
        """Test that an error is raised when field does not exist in the record type."""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        OUT_FILE = "will-not-be-generated_no_schema.lobster"
        test_runner.cmd_args.out = OUT_FILE
        rules = {
            "package": "extraction_test",
            "record-type": "base_type",
            "description-fields": ["does_not_exist_field"],
        }
        test_runner.config_file_data.conversion_rules = [rules]
        test_runner.declare_input_file(self._data_directory /
                                        "extraction_hierarchy.trlc")
        test_runner.declare_input_file(self._data_directory /
                                        "extraction_hierarchy.rsl")

        completed_process = test_runner.run_tool_test()
        print(completed_process.stderr)
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"lobster-trlc: successfully wrote 2 items to "
                                  f"{OUT_FILE}\n")
        asserter.assertExitCode(0)

    def test_to_string_missing(self):
        """Test that a missing to-string rule causes an error"""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "namespace": "req",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
        ]
        test_runner.config_file_data.to_string_rules = [
            {
                "package": "buildings",
                "tuple-type": "Thermal_Insolation",
                "to-string": ["abc"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertStdErrText(
            "lobster-trlc: error in 'to-string-rules' in config.yaml: No "
            "'to-string' function defined for tuple 'Building_Category' with value "
            "'{'floors': 3, 'name': 'school'}', used at to_string_test.trlc:5:16, "
            "defined at to_string_test.rsl:3:7!\n"
        )
        asserter.assertExitCode(1)

    def test_to_string_missing_no_schema(self):
        """Test that a missing to-string rule causes an error"""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated_no_schema.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
        ]
        test_runner.config_file_data.to_string_rules = [
            {
                "package": "buildings",
                "tuple-type": "Thermal_Insolation",
                "to-string": ["abc"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertStdErrText(
            "lobster-trlc: error in 'to-string-rules' in config.yaml: No "
            "'to-string' function defined for tuple 'Building_Category' with value "
            "'{'floors': 3, 'name': 'school'}', used at to_string_test.trlc:5:16, "
            "defined at to_string_test.rsl:3:7!\n"
        )
        asserter.assertExitCode(1)

    def test_tuple_member_does_not_exist(self):
        """Test that a to_string rule causes error if a tuple member does not exist."""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "namespace": "req",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
        ]
        test_runner.config_file_data.to_string_rules = [
            {
                "package": "buildings",
                "tuple-type": "Thermal_Insolation",
                "to-string": ["$(does_not_exist)"],
            },
            {
                "package": "buildings",
                "tuple-type": "Building_Category",
                "to-string": ["abc"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr(
            "lobster-trlc: error in 'to-string-rules' in config.yaml: All 'to_string' "
            "conversion functions failed for tuple 'Thermal_Insolation' with value"
        )
        asserter.assertExitCode(1)

    def test_tuple_member_does_not_exist_no_schema(self):
        """Test that a to_string rule causes error if a tuple member does not exist."""
        # lobster-trace: UseCases.TRLC_Config_File_Key_Error
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
        ]
        test_runner.config_file_data.to_string_rules = [
            {
                "package": "buildings",
                "tuple-type": "Thermal_Insolation",
                "to-string": ["$(does_not_exist)"],
            },
            {
                "package": "buildings",
                "tuple-type": "Building_Category",
                "to-string": ["abc"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr(
            "lobster-trlc: error in 'to-string-rules' in config.yaml: All 'to_string' "
            "conversion functions failed for tuple 'Thermal_Insolation' with value"
        )
        asserter.assertExitCode(1)

    def test_too_many_conversion_rules(self):
        """Test that orphan conversion rules are detected."""
        # lobster-trace: UseCases.TRLC_Config_File_non_existent_conversion_rules
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "namespace": "req",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
            {
                "package": "buildings",
                "record-type": "Does_Not_Exist",
                "namespace": "req",
                "description-fields": ["something"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr(
            "lobster-trlc: Invalid conversion rule defined in config.yaml: The "
            "following conversion rules do not match any record type in the TRLC "
            "symbol table: buildings.Does_Not_Exist.",
        )
        asserter.assertExitCode(1)

    def test_too_many_conversion_rules_no_schema(self):
        """Test that orphan conversion rules are detected."""
        # lobster-trace: UseCases.TRLC_Config_File_non_existent_conversion_rules
        test_runner = self.create_test_runner()
        test_runner.cmd_args.out = "will-not-be-generated_no_schema.lobster"
        test_runner.config_file_data.conversion_rules = [
            {
                "package": "buildings",
                "record-type": "Building",
                "description-fields": ["summary"],
                "tags": ["category", "thermal_insulation"],
            },
            {
                "package": "buildings",
                "record-type": "Does_Not_Exist",
                "description-fields": ["something"],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdOutText()
        asserter.assertInStdErr(
            "lobster-trlc: Invalid conversion rule defined in config.yaml: The "
            "following conversion rules do not match any record type in the TRLC "
            "symbol table: buildings.Does_Not_Exist.",
        )
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
