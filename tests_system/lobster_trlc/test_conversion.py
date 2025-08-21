from typing import Optional
from dataclasses import dataclass
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from tests_system.asserter import Asserter


@dataclass
class TestSetup:
    name: str
    num_expected_items: int
    record_type: str
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
                asserter.assertStdOutText(
                    f"lobster-trlc: successfully wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()

    def test_to_string_rules(self):
        """Test that to_string rules are applied correctly."""
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
        asserter.assertStdOutText(
            f"lobster-trlc: successfully wrote 4 items to {out_file}\n",
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
