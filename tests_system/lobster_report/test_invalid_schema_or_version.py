from .lobster_report_system_test_case_base import LobsterReportSystemTestCaseBase
from ..asserter import Asserter


class ReportInvalidSchemaOrVersionTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_invalid_schema(self):
        # lobster-trace: core_report_req.Invalid_Schema
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_invalid_schema.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_schema.lobster")

        self._test_runner.cmd_args.lobster_config = "lobster_invalid_schema.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertStdOutText("python_invalid_schema.lobster: "
                                  "lobster error: unknown schema kind "
                                  "invalid-schema-name\n\n"
                                  "lobster-lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_invalid_version(self):
        # lobster-trace: core_report_req.Invalid_Schema_Version
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_invalid_version.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_version.lobster")

        self._test_runner.cmd_args.lobster_config = "lobster_invalid_version.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertStdOutText("python_invalid_version.lobster: "
                                  "lobster error: version 99 for schema "
                                  "lobster-req-trace is not supported\n\n"
                                  "lobster-lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_invalid_json(self):
        # lobster-trace: core_report_req.Invalid_JSON_File
        self._test_runner.declare_input_file(self._data_directory /
                                             "lobster_invalid_json.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_invalid_json.lobster")

        self._test_runner.cmd_args.lobster_config = "lobster_invalid_json.conf"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertStdOutText("trlc_invalid_json.lobster:6:2: "
                                  "lobster error: Extra data\n\n"
                                  "lobster-lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)
