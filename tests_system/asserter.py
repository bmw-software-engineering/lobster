import json
from subprocess import CompletedProcess
from unittest import TestCase
from .test_runner import TestRunner


# pylint: disable=invalid-name


# Setting this flag will tell unittest not to print tracebacks from this frame.
# This way our custom assertions will show the interesting line number from the caller
# frame, and not from this boring file.
__unittest = True


class Asserter:
    def __init__(self, system_test_case: TestCase, completed_process: CompletedProcess,
                 test_runner: TestRunner):
        self._test_case = system_test_case
        self._completed_process = completed_process
        self._test_runner = test_runner

    def assertExitCode(self, expected: int, msg="Exit code differs"):
        # lobster-trace: system_test.Compare_Exit_Code
        self._test_case.assertEqual(
            expected,
            self._completed_process.returncode,
            msg,
        )

    def assertStdOutText(self, expected: str, msg="STDOUT differs"):
        # lobster-trace: system_test.Compare_Stdout
        self._test_case.assertEqual(expected, self._completed_process.stdout, msg)

    def assertStdErrText(self, expected: str, msg="STDERR differs"):
        # lobster-trace: system_test.Compare_Stderr
        self._test_case.assertEqual(expected, self._completed_process.stderr, msg)

    def assertNoStdErrText(self, msg="STDERR contains output"):
        self.assertStdErrText("", msg)

    def assertNoStdOutText(self, msg="STDOUT contains output"):
        self.assertStdOutText("", msg)

    def assertInStdErr(self, expected_substring: str,
                             msg="STDERR does not contain expected text"):
        """
        Assert that the expected_substring appears somewhere in the stderr output.
        """
        self._test_case.assertIn(
            expected_substring,
            self._completed_process.stderr,
            (
                f"{msg}\n"
                f"Expected to find: {expected_substring!r}\n"
                f"STDERR was: {self._completed_process.stderr!r}"
            )
        )

    def assertOutputFiles(self):
        """For each expected file, checks if an actual file has been created with the
        expected content

        Before comparing the actual text with the expected text, we do the
        following replacements:
        a) Replace Windows-like slashes \\ with / in order to be able to
           compare the actual output on all OS against the expected output on
           Linux
        b) Replace the fixed string CURRENT_WORKING_DIRECTORY with the absolute path to
           the current working directory. This is necessary for tools like
           lobster-cpptest which write absolute paths into their *.lobster
           output files.
        """
        # lobster-trace: system_test.Compare_Output_Files
        if not self._test_runner.tool_output_files:
            self._test_case.fail(
                "Invalid test setup: No expected output files have been registered."
            )

        for expected_file_ref in self._test_runner.tool_output_files:
            expected_location = self._test_runner.working_dir / expected_file_ref.name
            try:
                with open(
                    expected_file_ref,
                    "r",
                    encoding="UTF-8",
                ) as expected_file:
                    try:
                        with open(
                            expected_location,
                            "r",
                            encoding="UTF-8",
                        ) as actual_file:
                            # lobster-trace: system_test.Slashes
                            modified_actual = actual_file.read().replace("\\\\", "/")

                            # lobster-trace: system_test.CWD_Placeholder
                            modified_expected = expected_file.read().replace(
                                "CURRENT_WORKING_DIRECTORY",
                                str(self._test_runner.working_dir),
                            )
                            modified_actual_json = is_valid_json(modified_actual)
                            modified_expected_json = is_valid_json(modified_expected)
                            if modified_actual_json and modified_expected_json:
                                self._test_case.assertEqual(
                                    sort_json(modified_actual_json),
                                    sort_json(modified_expected_json),
                                    f'File differs from expectation '
                                    f'{expected_file_ref}!',
                                )
                            else:
                                self._test_case.assertEqual(
                                    modified_actual,
                                    modified_expected,
                                    f'File differs from expectation '
                                    f'{expected_file_ref}!',
                                )
                    except FileNotFoundError:
                        self._test_case.fail(f"File {expected_file_ref} was not "
                                             f"generated by the tool under test!")
            except FileNotFoundError as ex:
                self._test_case.fail(f"Invalid test setup: {ex}")


def is_valid_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return False


def sort_json(json_data):
    if isinstance(json_data, dict):
        return sorted((keys, sort_json(values)) for keys, values in json_data.items())
    if isinstance(json_data, list):
        return sorted(sort_json(items) for items in json_data)
    return json_data
