import sys
from posixpath import normpath
from os import scandir, DirEntry, remove
from os.path import basename, dirname, join
from pathlib import Path
from subprocess import CompletedProcess, PIPE, run
from typing import Iterator, Optional, List

from tests_utils.update_online_json_with_hashes import update_json

# This is the folder containing the folders starting with "rbt-"
REQUIREMENTS_BASED_TEST_PREFIX = "rbt-"
LOBSTER_ONLINE_REPORT_TOOL = "lobster-online-report"


class TestSetup:
    _INPUT_FOLDER_NAME = "input"
    _ARGS_FILE_NAME = "args.txt"
    _EXPECTED_OUTPUT_FOLDER_NAME = "expected-output"
    _EXIT_CODE_FILE_NAME = "exit-code.txt"
    _EXPECTED_STDOUT_FILE_NAME = "stdout.txt"
    _EXPECTED_STDERR_FILE_NAME = "stderr.txt"
    _LOBSTER_FILE_ENDING = ".lobster"

    def __init__(self, test_case_path: str):
        """Constructor

        :param test_case_path: the test case path. It must contain subdirectories
        called "input" and "expected-output".
        """
        self._input_folder = join(test_case_path, self._INPUT_FOLDER_NAME)
        self._test_case_path = test_case_path
        self._args = self._get_args()
        self._expected_exit_code = self._get_expected_exit_code()
        self._name = self._get_name(test_case_path)
        self._expected_lobster_output_file_names = \
            self._get_expected_lobster_output_file_names()

    @property
    def test_case_path(self) -> str:
        """Returns the path to the directory which contains the test case"""
        return self._test_case_path

    @property
    def expected_lobster_output_file_names(self) -> List[str]:
        """Returns a list of all file names of all expected lobster output files.

        The tool under test is expected to generate files with these names in the
        "input" folder.
        """
        return self._expected_lobster_output_file_names

    def get_expected_output_path(self) -> str:
        """Returns the path of the folder containing the expected output, which can be
        used to compare against the actual output"""
        return join(self._test_case_path, self._EXPECTED_OUTPUT_FOLDER_NAME)

    def _get_expected_lobster_output_file_names(self) -> List[str]:
        """Retrieves the expected file names of all lobster output files
        """
        return [
            dir_entry.name for dir_entry in scandir(self.get_expected_output_path())
            if (dir_entry.is_file() and
                dir_entry.name.endswith(self._LOBSTER_FILE_ENDING))
        ]

    @staticmethod
    def _get_name(test_case_path: str) -> str:
        """Creates a debug name for the test case, which consists of the RBT folder name
        and the test case folder name"""
        return join(basename(dirname(test_case_path)), basename(test_case_path))

    @property
    def args(self) -> List[str]:
        """Returns the command line arguments which must be used to start the tool under
        test"""
        return self._args

    @property
    def name(self) -> str:
        """Returns the name of the test case, which is equal to the folder name
        containing the test case"""
        return self._name

    @property
    def expected_exit_code(self) -> int:
        """Returns the expected exit code of the tool under test"""
        return self._expected_exit_code

    def _get_args(self) -> List[str]:
        """Reads the command line arguments (which must be used to start the tool under
        test) from the corresponding test setup file"""
        file = join(self._input_folder, self._ARGS_FILE_NAME)
        with open(file, "r", encoding="UTF-8") as file:
            return [argument.strip() for argument in file.readlines()]

    def get_expected_stdout(self) -> str:
        """Reads the expected command line output (for stdout) from the corresponding
        test setup file"""
        cmd_file = join(
            self.get_expected_output_path(),
            self._EXPECTED_STDOUT_FILE_NAME,
        )
        with open(cmd_file, "r", encoding="UTF-8") as file:
            return file.read()

    def get_expected_stderr(self) -> str:
        """Reads the expected command line output (for stderr) from the corresponding
        test setup file"""
        errout_file = join(
            self.get_expected_output_path(),
            self._EXPECTED_STDERR_FILE_NAME,
        )
        with open(errout_file, "r", encoding="UTF-8") as file:
            return file.read()

    @property
    def input_folder(self) -> str:
        """Returns the path containing the input data for the test"""
        return self._input_folder

    def _get_expected_exit_code(self) -> int:
        """Returns the expectation of the tool exit code"""
        expected_exit_code_file = join(
            self._test_case_path,
            self._EXPECTED_OUTPUT_FOLDER_NAME,
            self._EXIT_CODE_FILE_NAME,
        )
        with open(expected_exit_code_file, "r", encoding="UTF-8") as file:
            return int(file.readline())


def _run_test(setup: TestSetup, tool: str) -> CompletedProcess:
    """Runs the tool system test using the coverage command.
    The tool will be executed such that its current working directory is equal to the
    "input" folder."""
    print(f"Starting system test '{setup.name}' with arguments {setup.args} "
          f"for tool '{tool}' with coverage.")
    root_directory = Path(__file__).resolve().parents[1]
    coverage_command = [
        "coverage", "run", "-p",
        f"--rcfile={root_directory / 'coverage.cfg'}",
        "--branch",
        f"--data-file={root_directory / '.coverage'}",
        f"--source={root_directory / 'lobster'}",
        tool, *setup.args
    ]

    completed_process = run(
        coverage_command,
        stdout=PIPE,
        stderr=PIPE,
        encoding="UTF-8",
        cwd=setup.input_folder,
        check=False,
    )
    return completed_process


def _compare_cmd_output(name: str, expected: str, actual: str) -> bool:
    if expected != actual:
        print(f"Actual {name} is (length: {len(actual)} chars):\n{actual}")
        print(f"Expected {name} is (length: {len(expected)} chars):\n{expected}")
        return False
    return True


def _compare_results(setup: TestSetup, completed_process: CompletedProcess):
    assert _compare_cmd_output(
        name="STDOUT",
        expected=setup.get_expected_stdout(),
        actual=completed_process.stdout,
    ), "Command line output for STDOUT is different!"

    assert _compare_cmd_output(
        name="STDERR",
        expected=setup.get_expected_stderr(),
        actual=completed_process.stderr,
    ), "Command line output for STDERR is different!"

    assert setup.expected_exit_code == completed_process.returncode, \
        f"{setup.name}: Expected exit code is {setup.expected_exit_code}, " \
        f"actual is {completed_process.returncode}!"

    for expected_lobster_output_file_name in setup.expected_lobster_output_file_names:
        expected = join(
            setup.get_expected_output_path(),
            expected_lobster_output_file_name,
        )
        actual = join(setup.input_folder, expected_lobster_output_file_name)
        _compare_lobster_files(expected, actual, setup.test_case_path)


def _compare_lobster_files(expected: str, actual: str, test_case_path: str):
    """Compares an actual LOBSTER file with an expected LOBSTER file

    Before comparing the actual text with the expected text, we do the
    following replacements:
    a) Replace Windows-like slashes \\ with / in order to be able to
        compare the actual output on all OS against the expected output on
        Linux
    b) Replace the fixed string TEST_CASE_PATH with the absolute path to
        the current test case directory. This is necessary for tools like
        lobster-cpptest which write absolute paths into their *.lobster
        output files.

    :param expected: The path to the file containing the expected output
    :param actual: The path to the file containing the actual output
    :param test_case_path: The path containing the test case files
    """
    with open(expected, "r", encoding="UTF-8") as expected_lobster_file:
        try:
            with open(actual, "r", encoding="UTF-8") as actual_lobster_file:
                modified_actual = actual_lobster_file.read().replace("\\\\", "/")
                modified_expected = expected_lobster_file.read().replace(
                    "TEST_CASE_PATH", test_case_path
                )
                assert modified_actual == modified_expected, \
                    f"Actual *.lobster file differs from expectation {expected}!"
        except FileNotFoundError as ex:
            assert True, \
                f"File {ex.filename} was not generated by the tool under test!"


def _get_directories(start_directory: Path,
                     startswith: Optional[str] = None) -> Iterator[DirEntry]:
    """Returns DirEntry instances for each subdirectory found in the given start
    directory

    :param startswith: the path to a directory in which to search for nested directories
    :param startswith: an optional filter criteria for names of nested directories. If
    given, then only subdirectories starting with this prefix are returned by the
    Iterator
    """
    if not start_directory:
        raise ValueError("No start directory specified!")
    for dir_entry in scandir(start_directory):
        if dir_entry.is_dir():
            if (not startswith) or dir_entry.name.startswith(startswith):
                yield dir_entry


def _delete_generated_files(setup: TestSetup):
    """Deletes the *.lobster file that has been generated by the test"""
    for expected_lobster_output_file_name in setup.expected_lobster_output_file_names:
        generated = join(
            setup.input_folder,
            expected_lobster_output_file_name,
        )
        print(f"DELETING {generated}")
        try:
            remove(generated)
        except FileNotFoundError:
            pass


def _run_tests(directory: Path, tool: str) -> int:
    """Runs all system tests in the given folder for the specified tool.

    :param directory: the path to the directory containing all test cases
    :param tool: the path to the Python file where the tool main function is
    implemented, and which shall be tested.
    """
    if not directory:
        raise ValueError("No directory specified!")
    if not tool:
        raise ValueError("No tool specified!")

    counter = 0
    for rbt_dir_entry in _get_directories(directory, REQUIREMENTS_BASED_TEST_PREFIX):
        for test_case_dir_entry in _get_directories(rbt_dir_entry.path):
            test_setup = TestSetup(test_case_dir_entry.path)
            completed_process = _run_test(test_setup, tool)
            if basename(tool) == LOBSTER_ONLINE_REPORT_TOOL:
                for file_name in test_setup.expected_lobster_output_file_names:
                    expected = join(
                        test_setup.get_expected_output_path(),
                        file_name,
                    )
                    update_json(expected)
            _compare_results(test_setup, completed_process)
            _delete_generated_files(test_setup)
            counter += 1
    print(f"{counter} system tests finished successfully for {tool}.")

    return 0


def _get_tool(test_dir: Path) -> str:
    """Determines the path to the tool which shall be tested, given the test case path.

    The tool under test is determined by assuming that the parent folder name is equal
    to the tool name
    :param test_dir: The path containing the requirements-based tests
    """
    return normpath(Path(join("../", basename(test_dir))).absolute())


if __name__ == "__main__":
    test_directory = Path(sys.argv[1]).resolve()
    print(f"Starting system tests on folder '{test_directory}'")

    sys.exit(
        _run_tests(
            test_directory,
            _get_tool(test_directory),
        ),
    )
