import os
from tempfile import NamedTemporaryFile
from dataclasses import dataclass
from typing import Tuple, Type
import unittest
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_system_test_case_base import (
        LobsterMetaDataToolBaseSystemTestCaseBase
    )
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_asserters import (
        SpecificAsserter,
        HelpAsserter,
        VersionAsserter,
    )
from tests_system.asserter import Asserter
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_test_runner import IMPLEMENTATION_MESSAGE


class ToolBaseTest(LobsterMetaDataToolBaseSystemTestCaseBase):
    def setUp(self) -> None:
        super().setUp()
        self._test_runner = self.create_test_runner()

    @dataclass
    class ArgumentSetup:
        argument_variants: Tuple[str, str]
        asserter_cls: Type[SpecificAsserter]

    def test_early_exit_arguments(self):
        """Test that 'help' and 'version' cmd arguments trigger early exit

           This test also verifies the behavior with respect to combinations
           of these arguments, e.g. `--help --version` or `--version -h`.
           The first argument defines whether to expect the help or version message.
        """
        setups = (
            self.ArgumentSetup(
                argument_variants=("--help", "-h"),
                asserter_cls=HelpAsserter,
            ),
            self.ArgumentSetup(
                argument_variants=("--version", "-v"),
                asserter_cls=VersionAsserter,
            ),
        )

        for i, first_setup in enumerate(setups):
            for first_argument in first_setup.argument_variants:
                for second_argument in (
                        None,
                        *(setups[not i].argument_variants),
                        "--other-arg",
                ):
                    self._test_runner.cmd_args.reset()
                    self._test_runner.cmd_args.append_arg(first_argument)
                    if second_argument:
                        self._test_runner.cmd_args.append_arg(second_argument)

                    with self.subTest(f"args={self._test_runner.cmd_args.as_list()}, "
                                      f"asserter={first_setup.asserter_cls.__name__}"):
                        completed_process = self._test_runner.run_tool_test()
                        first_setup.asserter_cls(
                            self, completed_process, self._test_runner
                        ).assert_result()

    def test_no_arguments(self):
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(IMPLEMENTATION_MESSAGE + "\n")
        asserter.assertExitCode(0)

    def test_invalid_arguments(self):
        self._test_runner.cmd_args.append_arg("--invalid-arg")
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn(
            "apple: error: unrecognized arguments: --invalid-arg",
            completed_process.stderr,
        )
        asserter.assertNoStdOutText()
        asserter.assertExitCode(2)

    def test_args_from_file(self):
        """Test that the version argument can be loaded from a file

           If loading the version argument from a file works, then we assume it works
           for all other arguments, too.
        """
        # lobster-trace: req.Args_From_File

        # with NamedTemporaryFile and Python 3.12+ we could simply use
        # delete_on_close=False and delete=True, but we want to support Python 3.8+

        with NamedTemporaryFile(
            mode="w",
            encoding="UTF-8",
            delete=False,  # Use delete=False for compatibility with Python 3.8+
        ) as tmp_file:
            tmp_file.write("--version\n")
            tmp_file.flush()
            tmp_file_path = tmp_file.name

        try:
            self._test_runner.cmd_args.append_arg(f"@{tmp_file_path}")
            completed_process = self._test_runner.run_tool_test()
            asserter = VersionAsserter(self, completed_process, self._test_runner)
            asserter.assert_result()
        finally:
            os.remove(tmp_file_path)


if __name__ == "__main__":
    unittest.main()
