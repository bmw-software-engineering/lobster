from dataclasses import dataclass
from .lobster_system_test_case_base import LobsterTrlcSystemTestCaseBase
from ..asserter import Asserter


class InputFromFilesTest(LobsterTrlcSystemTestCaseBase):
    def test_base_and_extended(self):
        @dataclass
        class TestSetup:
            name: str
            num_expected_items: int

        test_setups = [
            TestSetup(
                name="base_and_extended",
                num_expected_items=2,
            ),
            TestSetup(
                name="extended_only",
                num_expected_items=1,
            ),
        ]

        for setup in test_setups:
            with self.subTest(setup=setup.name):
                test_runner = self.create_test_runner()
                test_runner.declare_trlc_config_file(
                    self._data_directory / f"extraction_hierarchy_{setup.name}.conf",
                )
                out_file = f"extraction_hierarchy_{setup.name}.out.lobster"
                test_runner.cmd_args.out = out_file
                test_runner.declare_output_file(self._data_directory / out_file)
                test_runner.config_file_data.inputs = [
                    "extraction_hierarchy.trlc",
                    "extraction_hierarchy.rsl",
                ]
                for file in test_runner.config_file_data.inputs:
                    test_runner.copy_file_to_working_directory(
                        self._data_directory / file,
                    )
                completed_process = test_runner.run_tool_test()
                asserter = Asserter(self, completed_process, test_runner)
                asserter.assertNoStdErrText()
                asserter.assertStdOutText(
                    f"lobster-trlc: successfully wrote {setup.num_expected_items} "
                    f"items to {out_file}\n",
                )
                asserter.assertExitCode(0)
                asserter.assertOutputFiles()
