import unittest
from tests_system.lobster_trlc.lobster_system_test_case_base import (
    LobsterTrlcSystemTestCaseBase)


class InputNotFileNotDirectoryTest(LobsterTrlcSystemTestCaseBase):
    """The goal of this test is to check that the tool aborts if one of the input
       paths does not exist (neither a file nor a directory)."""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()
        self._test_runner.config_file_data.conversion_rules = [
            self.NAMASTE_CONVERSION_RULE,
        ]

    def test_path_does_not_exist(self):
        # lobster-trace: trlc_req.Input_Not_File_Not_Directory
        self._test_runner.config_file_data.inputs.append("file_does_not_exist.trlc")
        with self.assertRaises(ValueError) as ctx:
            self._test_runner.run_tool_test()
        self.assertIn("file_does_not_exist.trlc", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
