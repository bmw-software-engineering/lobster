from dataclasses import dataclass
from typing import Tuple, Type
from .lobster_meta_data_tool_base_system_test_case_base import (
    LobsterMetaDataToolBaseSystemTestCaseBase,
)
from .lobster_meta_data_tool_base_asserters import (
    SpecialAsserter, HelpAsserter, VersionAsserter, IMPLEMENTATION_MESSAGE
)
from ..asserter import Asserter


class ToolBaseTest(LobsterMetaDataToolBaseSystemTestCaseBase):
    def setUp(self) -> None:
        super().setUp()
        self._test_runner = self.create_test_runner()

    @dataclass
    class ArgumentSetup:
        argument_variants: Tuple[str, str]
        asserter_cls: Type[SpecialAsserter]

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
