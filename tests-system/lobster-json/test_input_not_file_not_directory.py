from .lobsterjsonsystemtestcasebase import LobsterJsonSystemTestCaseBase
from ..asserter import Asserter


# The goal of these test cases is to check if an error message gets printed
# if one of the input files to the lobster-json tool does not exist.
#
# There are two test setups:
# - one that uses only paths to files that do not exist
# - one that uses two paths, where one exists and the other does not.
#
# Note regarding test setup:
# The parameter `--out` is omitted, because the expectation is that, no lobster output
# is generated.
# By omitting `--out` any output will be written to `STDOUT`.
# This way we can verify that indeed no lobster output is generated.
# The tool could create output for the valid paths, and ignore the invalid paths.
# This would violate the requirements, and any such behavior should be detected.

class InputNotFileNotDirectoryTest(LobsterJsonSystemTestCaseBase):
    _FILE_DOES_NOT_EXIST = "file_does_not_exist.json"

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.inputs.append(self._FILE_DOES_NOT_EXIST)
        self._test_runner.config_file_data.tag_attribute = "pizza"

    def test_nothing_exists(self):
        # lobster-trace: json_req.Input_Not_File_Not_Directory
        asserter = Asserter(self, self._test_runner.run_tool_test(), self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster error: {self._FILE_DOES_NOT_EXIST} is not a file or "
            f"directory\n"
        )
        asserter.assertExitCode(1)

    def test_one_file_exists(self):
        # lobster-trace: json_req.Input_Not_File_Not_Directory
        self._test_runner.declare_input_file(self._data_directory / "valid-mini.json")
        asserter = Asserter(self, self._test_runner.run_tool_test(), self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"<config>: lobster error: {self._FILE_DOES_NOT_EXIST} is not a file or "
            f"directory\n"
        )
        asserter.assertExitCode(1)
