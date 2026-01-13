from typing import Optional, List
from dataclasses import dataclass
import unittest
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


@dataclass
class TestSetup:
    name: str
    num_expected_items: int
    record_type: Optional[str] = None
    rules: Optional[List] = None
    out_file: Optional[str] = None
    applies_to_derived_types: Optional[bool] = None


class ConversionRuleTest(LobsterTrlcSystemTestCaseBase):
    def test_rule_propagation(self):
        """Test that rules are propagated to extended record types."""
        test_setups = [
            TestSetup(
                name="base_and_extended",
                num_expected_items=2,
                record_type="base_type",
            ),
            TestSetup(
                name="extended_only",
                num_expected_items=1,
                record_type="extended_type",
            ),
        ]
        # create copies of the above setups,
        # but with explicit values for 'applies_to_derived_types'
        test_setups.extend([
            TestSetup(
                name=setup.name,
                num_expected_items=setup.num_expected_items,
                record_type=setup.record_type,
                applies_to_derived_types=True,
            ) for setup in test_setups
        ])
        # add a setup for the base type only
        test_setups.append(
            TestSetup(
                name="base_only",
                num_expected_items=1,
                record_type="base_type",
                applies_to_derived_types=False,
            )
        )

        for setup in test_setups:
            with self.subTest(setup=setup.name):
                # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
                out_file = f"extraction_hierarchy_{setup.name}.out.lobster"
                test_runner = self.create_test_runner()
                test_runner.cmd_args.out = out_file
                test_runner.declare_output_file(self._data_directory / out_file)
                rules = {
                    "package": "extraction_test",
                    "record-type": setup.record_type,
                    "namespace": "req",
                    "description-fields": ["description"],
                }
                if setup.applies_to_derived_types is not None:
                    rules["applies-to-derived-types"] = setup.applies_to_derived_types
                test_runner.config_file_data.conversion_rules = [rules]
                test_runner.declare_input_file(self._data_directory /
                                               "extraction_hierarchy.trlc")
                test_runner.declare_input_file(self._data_directory /
                                               "extraction_hierarchy.rsl")

                completed_process = test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, test_runner)
                asserter.assertNoStdErrText()
                lobster_schema = "lobster-req-trace"
                lobster_version = 4
                asserter.assertStdOutText(
                    f"Lobster file version {lobster_version} containing 'schema' = '{lobster_schema}' is deprecated, "
                    f"please migrate to version 5\n"
                    f"lobster-trlc: successfully wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()

    def test_rule_propagation_no_schema(self):
        """Test that rules are propagated to extended record types."""
        test_setups = [
            TestSetup(
                name="base_and_extended",
                num_expected_items=2,
                record_type="base_type",
            ),
            TestSetup(
                name="extended_only",
                num_expected_items=1,
                record_type="extended_type",
            ),
        ]
        # create copies of the above setups,
        # but with explicit values for 'applies_to_derived_types'
        test_setups.extend([
            TestSetup(
                name=setup.name,
                num_expected_items=setup.num_expected_items,
                record_type=setup.record_type,
                applies_to_derived_types=True,
            ) for setup in test_setups
        ])
        # add a setup for the base type only
        test_setups.append(
            TestSetup(
                name="base_only",
                num_expected_items=1,
                record_type="base_type",
                applies_to_derived_types=False,
            )
        )

        for setup in test_setups:
            with self.subTest(setup=setup.name):
                # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
                out_file = f"extraction_hierarchy_{setup.name}.out_no_schema.lobster"
                test_runner = self.create_test_runner()
                test_runner.cmd_args.out = out_file
                test_runner.declare_output_file(self._data_directory / out_file)
                rules = {
                    "package": "extraction_test",
                    "record-type": setup.record_type,
                    "description-fields": ["description"],
                }
                if setup.applies_to_derived_types is not None:
                    rules["applies-to-derived-types"] = setup.applies_to_derived_types
                test_runner.config_file_data.conversion_rules = [rules]
                test_runner.declare_input_file(self._data_directory /
                                               "extraction_hierarchy.trlc")
                test_runner.declare_input_file(self._data_directory /
                                               "extraction_hierarchy.rsl")

                completed_process = test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, test_runner)
                asserter.assertNoStdErrText()
                asserter.assertStdOutText(
                    f"lobster-trlc: wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()

    def test_to_string_rules(self):
        """Test that to_string rules are applied correctly."""
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        test_runner = self.create_test_runner()
        out_file = "to_string_rules.out.lobster"
        test_runner.cmd_args.out = out_file
        test_runner.declare_output_file(self._data_directory / out_file)
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
                "to-string": ["FACTOR=$(thermal_factor), THICKNESS=$(thickness)!"],
            },
            {
                "package": "buildings",
                "tuple-type": "Building_Category",
                "to-string": [
                    "$(name) FLOORS=$(floors)",
                    "$(name) FLOORS=just-too-many",
                ],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        lobster_schema = "lobster-req-trace"
        lobster_version = 4
        asserter.assertStdOutText(
            f"Lobster file version {lobster_version} containing 'schema' = '{lobster_schema}' is deprecated, "
            f"please migrate to version 5\n"
            f"lobster-trlc: successfully wrote 4 items to {out_file}\n",
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_to_string_rules_no_schema(self):
        """Test that to_string rules are applied correctly."""
        # lobster-trace: UseCases.Incorrect_data_Extraction_from_TRLC
        test_runner = self.create_test_runner()
        out_file = "to_string_rules.out_no_schema.lobster"
        test_runner.cmd_args.out = out_file
        test_runner.declare_output_file(self._data_directory / out_file)
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
                "to-string": ["FACTOR=$(thermal_factor), THICKNESS=$(thickness)!"],
            },
            {
                "package": "buildings",
                "tuple-type": "Building_Category",
                "to-string": [
                    "$(name) FLOORS=$(floors)",
                    "$(name) FLOORS=just-too-many",
                ],
            },
        ]
        test_runner.declare_input_file(self._data_directory / "to_string_test.trlc")
        test_runner.declare_input_file(self._data_directory / "to_string_test.rsl")

        completed_process = test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"lobster-trlc: wrote 4 items to {out_file}\n",
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_tag_version(self):
        base_rule = {
            "package": "test_reqs",
            "record-type": "featReq",
            "namespace": "req",
            "description-fields": ["description"],
        }
        test_setups = [
            # lobster-trace: trlc_req.Tag_Version_From_Record_Field
            TestSetup(
                name="version_field_configured_return_value",
                num_expected_items=2,
                rules=[{**base_rule, "version-field": "version"}],
                out_file="reqs_tag_version_value.out.lobster",
            ),
            # lobster-trace: trlc_req.Tag_Version_None_If_Field_Missing
            TestSetup(
                name="version_field_not_configured_return_none",
                num_expected_items=2,
                rules=[base_rule],
                out_file="reqs_tag_version_none.out.lobster",
            ),
            # lobster-trace: trlc_req.Tag_Version_None_If_Not_Configured
            TestSetup(
                name="version_field_mis_configured_return_none",
                num_expected_items=2,
                rules=[{**base_rule, "version-field": "versino"}],
                out_file="reqs_tag_version_none.out.lobster",
            ),
        ]

        for setup in test_setups:
            with self.subTest(setup=setup.name):
                out_file = setup.out_file
                test_runner = self.create_test_runner()
                test_runner.cmd_args.out = out_file
                test_runner.config_file_data.conversion_rules = setup.rules
                test_runner.declare_output_file(self._data_directory / out_file)
                test_runner.declare_input_file(self._data_directory / "reqs.rsl")
                test_runner.declare_input_file(self._data_directory / "reqs.trlc")

                completed_process = test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, test_runner)
                asserter.assertNoStdErrText()
                lobster_schema = "lobster-req-trace"
                lobster_version = 4
                asserter.assertStdOutText(
                    f"Lobster file version {lobster_version} containing 'schema' = '{lobster_schema}' is deprecated, "
                    f"please migrate to version 5\n"
                    f"lobster-trlc: successfully wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()

    def test_tag_version_no_schema(self):
        base_rule = {
            "package": "test_reqs",
            "record-type": "featReq",
            "description-fields": ["description"],
        }
        test_setups = [
            # lobster-trace: trlc_req.Tag_Version_From_Record_Field
            TestSetup(
                name="version_field_configured_return_value",
                num_expected_items=2,
                rules=[{**base_rule, "version-field": "version"}],
                out_file="reqs_tag_version_value.out_no_schema.lobster",
            ),
            # lobster-trace: trlc_req.Tag_Version_None_If_Field_Missing
            TestSetup(
                name="version_field_not_configured_return_none",
                num_expected_items=2,
                rules=[base_rule],
                out_file="reqs_tag_version_none.out_no_schema.lobster",
            ),
            # lobster-trace: trlc_req.Tag_Version_None_If_Not_Configured
            TestSetup(
                name="version_field_mis_configured_return_none",
                num_expected_items=2,
                rules=[{**base_rule, "version-field": "versino"}],
                out_file="reqs_tag_version_none.out_no_schema.lobster",
            ),
        ]

        for setup in test_setups:
            with self.subTest(setup=setup.name):
                out_file = setup.out_file
                test_runner = self.create_test_runner()
                test_runner.cmd_args.out = out_file
                test_runner.config_file_data.conversion_rules = setup.rules
                test_runner.declare_output_file(self._data_directory / out_file)
                test_runner.declare_input_file(self._data_directory / "reqs.rsl")
                test_runner.declare_input_file(self._data_directory / "reqs.trlc")

                completed_process = test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, test_runner)
                asserter.assertNoStdErrText()
                asserter.assertStdOutText(
                    f"lobster-trlc: wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()


if __name__ == "__main__":
    unittest.main()
