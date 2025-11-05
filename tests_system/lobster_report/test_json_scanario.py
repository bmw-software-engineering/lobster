import unittest
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

        conf_file = "invalid_json.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"{conf_file}: lobster warning: configuration file format '.conf' "
                                  "is deprecated, please migrate to '.yaml' format\n"
                                  "trlc_invalid_json.lobster:6:2: "
                                  "lobster error: Extra data\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_invalid_json_yaml(self):
        # lobster-trace: core_report_req.Invalid_JSON_File
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_json.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_json.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_json.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_invalid_json.lobster:6:2: "
                                  "lobster error: Extra data\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_missing_config_file(self):
        # lobster-trace: core_report_req.File_Not_Found
        missing_file = "non_existent_input.conf"
        self._test_runner.cmd_args.lobster_config = missing_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"Config file not found: {missing_file}\n"
        )
        asserter.assertExitCode(1)

    def test_missing_config_file_yaml(self):
        # lobster-trace: core_report_req.File_Not_Found
        missing_file = "non_existent_input.yaml"
        self._test_runner.cmd_args.lobster_config = missing_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "non_existent_input.yaml: lobster error: Failed to validate yaml config file: "
            "[Errno 2] No such file or directory: 'non_existent_input.yaml'\n"
            "\n"
            "lobster-report: aborting due to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_unsupported_config_file(self):
        # lobster-trace: core_report_req.File_Not_Found
        missing_file = "non_existent_input.lobster"
        self._test_runner.cmd_args.lobster_config = missing_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            "non_existent_input.lobster: lobster error: configuration file format is "
            "unsupported, please use '.yaml' format\n"
            "\n"
            "lobster-report: aborting due to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_lobster_exception_dump(self):
        # lobster-trace: core_report_req.Lobster_Exception_Dump_Invalid_Input
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_input.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_input.lobster")

        conf_file = "invalid_input.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            "is deprecated, please migrate to '.yaml' format\n"
            "LOBSTER Error: location data does not contain 'kind'\n"
            "------------------------------------------------------------\n"
            "{'column': None, 'file': '.\\\\software.py', 'line': 1}\n"
            "------------------------------------------------------------\n"
        )
        asserter.assertExitCode(1)

    def test_lobster_exception_dump_yaml(self):
        # lobster-trace: core_report_req.Lobster_Exception_Dump_Invalid_Input
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_input.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_input.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_input.yaml"

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

        conf_file = "json_not_dict.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(f"{conf_file}: lobster warning: configuration file format '.conf' "
                                  "is deprecated, please migrate to '.yaml' format\n"
                                  "trlc_json_not_dict.lobster: "
                                  "lobster error: parsed json is not an object\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_invalid_json_not_dict_yaml(self):
        # lobster-trace: core_report_req.Invalid_JSON_Not_Dict
        self._test_runner.declare_input_file(self._data_directory /
                                             "json_not_dict.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_json_not_dict.lobster")

        self._test_runner.cmd_args.lobster_config = "json_not_dict.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_json_not_dict.lobster: "
                                  "lobster error: parsed json is not an object\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
