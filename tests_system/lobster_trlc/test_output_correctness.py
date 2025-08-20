from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)
from asserter import Asserter


class OutputCorrectnessTest(LobsterTrlcSystemTestCaseBase):
    """These tests verify the correctness of the output LOBSTER files"""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_output_correctness(self):
        """Test that output is correlated to input.

           This tests uses data where each value is used only once in the whole input
           set, so we can verify that each output item is populated with data only
           based on one single input item.
        """
        self._test_runner.cmd_args.out = "output_correctness_test.out.lobster"
        self._test_runner.declare_output_file(
            self._data_directory / self._test_runner.cmd_args.out)

        config = self._test_runner.config_file_data

        config.inputs_from_file = "output_correctness_test_inputs.txt"
        for file in (
            "output_correctness_test.rsl",
            config.inputs_from_file,
        ):
            self._test_runner.copy_file_to_working_directory(
                self._data_directory / file,
            )

        for file in (
            "output_correctness_test_a.trlc",
            "output_correctness_test_b.trlc",
        ):
            self._test_runner.declare_input_file(self._data_directory / file)

        config.conversion_rules = [
            {
                "package": "output_correctness_test",
                "record-type": "TheType",
                "namespace": "req",
                "description-fields": [
                    "string",
                    "integer",
                    "decimal",
                    "boolean",
                    "strings",
                    "decimals",
                    "booleans",
                    "integers",
                    "references",
                ],
            }
        ]
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "lobster-trlc: successfully wrote 5 items to "
            "output_correctness_test.out.lobster\n",
        )
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
