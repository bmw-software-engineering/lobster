from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase)


class ReportInvalidJsonTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_invalid_json(self):
        # lobster-trace: core_report_req.Invalid_JSON_File
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_json.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_json.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_json.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_invalid_json.lobster:6:2: "
                                  "lobster error: Extra data\n\n"
                                  "lobster-lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_missing_input_file(self):
        # lobster-trace: core_report_req.File_Not_Found
        missing_file = "non_existent_input.lobster"
        self._test_runner.cmd_args.lobster_config = missing_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"Config file not found: {missing_file}\n"
        )
        asserter.assertExitCode(1)

    def test_lobster_exception_dump(self):
        # lobster-trace: core_report_req.Lobster_Exception_Dump_Invalid_Input
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_input.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_input.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_input.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "LOBSTER Error: location data does not contain 'kind'\n"
            "------------------------------------------------------------\n"
            "{'column': None, 'file': '.\\\\software.py', 'line': 1}\n"
            "------------------------------------------------------------\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_json_not_dict(self):
        # lobster-trace: core_report_req.Invalid_JSON_Not_Dict
        self._test_runner.declare_input_file(self._data_directory /
                                             "json_not_dict.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_json_not_dict.lobster")

        self._test_runner.cmd_args.lobster_config = "json_not_dict.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_json_not_dict.lobster: "
                                  "lobster error: parsed json is not an object\n\n"
                                  "lobster-lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)
