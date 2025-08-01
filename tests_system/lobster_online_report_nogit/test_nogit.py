import json
import re
from .lobster_online_report_nogit_system_test_case_base import (
    LobsterOnlineReportNogitSystemTestCaseBase
)
from ..asserter import Asserter


class OnlineReportNogitTest(LobsterOnlineReportNogitSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def _create_dummy_files(self, lobster_file: str):
        """Reads a LOBSTER file and creates one dummy file with a unique name for each
           item in each level."""

        with open(self._data_directory / lobster_file, "r", encoding="UTF-8") as file:
            data = json.load(file)

        found_non_file_locations = False

        needed_dummy_files = set()
        for level in data["levels"]:
            for item in level["items"]:
                location = item["location"]
                if location["kind"] == "file":
                    item_file_name = location["file"]
                    if item_file_name in needed_dummy_files:
                        self.fail(f"Invalid test data: file name '{item_file_name}' "
                                  f"used multiple times in {lobster_file}!")
                    needed_dummy_files.add(item_file_name)
                else:
                    found_non_file_locations = True

        if not found_non_file_locations:
            self.fail(f"Invalid test data: The file '{lobster_file}' must contain at "
                      f"least one location that is not a File_Reference, because the "
                      f"test shall also verify that non-file locations are not "
                      f"touched!")

        for file_name in needed_dummy_files:
            destination = self._test_runner.working_dir / file_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.touch()

    def test_path_replacement(self):
        """Test that file paths (and only them) are replaced with remote URLs"""

        MAXI_LOBSTER = "maxi.lobster"
        self._create_dummy_files(MAXI_LOBSTER)

        for input_file_name, remote_url, commit in (
                ("mini.lobster", "https://Kronos.Beta.Quadrant", "0" * 40),
                (MAXI_LOBSTER, "https://plate.cup.fork", "spoon" * 8),
        ):
            with self.subTest(input_file_name=input_file_name):
                output_file_name = input_file_name.replace(".", "-expected.")
                input_file_path = self._data_directory / input_file_name
                self._test_runner.declare_input_file(input_file_path)
                self._test_runner.declare_output_file(
                    self._data_directory / output_file_name,
                )

                cmd_args = self._test_runner.cmd_args
                cmd_args.out = output_file_name
                cmd_args.lobster_report = str(input_file_path)
                cmd_args.commit = commit
                cmd_args.repo_root = str(self._test_runner.working_dir)
                cmd_args.remote_url = remote_url

                completed_process = self._test_runner.run_tool_test()

                asserter = Asserter(self, completed_process, self._test_runner)
                asserter.assertNoStdErrText()
                asserter.assertStdOutText(
                    f"LOBSTER report {output_file_name} created, "
                    f"using remote URL references.\n",
                )
                asserter.assertOutputFiles()
                asserter.assertExitCode(0)

    def test_no_arguments(self):
        """Test that running without any arguments fails with an error."""
        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(2)

    def test_one_argument_missing(self):
        """Test running with one missing argument fails with an error"""
        cmd_args = self._test_runner.cmd_args

        def init_args_except_one(exception_arg: str):
            for cmd_arg in vars(cmd_args).keys():
                if cmd_arg == exception_arg:
                    setattr(cmd_args, cmd_arg, None)
                else:
                    setattr(cmd_args, cmd_arg, f"dummy_value_for_{cmd_arg}")

        for missing_argument in vars(cmd_args).keys():
            with self.subTest(missing_argument=missing_argument):
                init_args_except_one(missing_argument)
                completed_process = self._test_runner.run_tool_test()

                # We compare the actual error message with the expected one,
                # but we want to ignore dashes and underscores in the cmd argument
                # names, to simplify the test. They are not important.
                # Note that named arguments have leading dashes, but positional
                # arguments do not.
                # The 'missing_argument' variable does not reflect dashes properly.
                # Our solution here is to ignore dashes and underscores in the full
                # string.
                std_err_no_dash = re.sub(r"[-_]", "", completed_process.stderr).lower()
                self.assertIn(f"error: the following arguments are required: "
                              f"{missing_argument.replace('_', '')}", std_err_no_dash)
                asserter = Asserter(self, completed_process, self._test_runner)
                asserter.assertNoStdOutText()
                asserter.assertExitCode(2)

    def test_input_file_not_found(self):
        input_file = "does_not_exist.lobster"
        cmd_args = self._test_runner.cmd_args
        cmd_args.out = "output.lobster"
        cmd_args.lobster_report = input_file
        cmd_args.commit = "12" * 20
        cmd_args.repo_root = "some/path"
        cmd_args.remote_url = "https://Bajor.Alpha.Quadrant"

        completed_process = self._test_runner.run_tool_test()

        asserter = Asserter(self, completed_process, self._test_runner)
        self.assertIn(
            f"No such file or directory: '{input_file}'",
            completed_process.stderr,
        )
        asserter.assertNoStdOutText()
        asserter.assertExitCode(1)

    def test_referenced_file_not_found(self):
        cmd_args = self._test_runner.cmd_args
        cmd_args.out = "output.lobster"
        cmd_args.lobster_report = str(self._data_directory / "invalid-ref.lobster")
        cmd_args.commit = "abc"
        cmd_args.repo_root = str(self._test_runner.working_dir)
        cmd_args.remote_url = "https://A.B.C"
        completed_process = self._test_runner.run_tool_test()

        asserter = Asserter(self, completed_process, self._test_runner)
        expected_path = str(self._test_runner.working_dir)
        asserter.assertStdErrText(
            f"Error: File 'does-not-exist.file' does not exist.\n"
            f"Note: Relative paths are resolved with respect to the "
            f"current working directory '{expected_path}'.\n",
        )
        asserter.assertNoStdOutText()
        asserter.assertExitCode(1)
