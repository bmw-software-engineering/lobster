import unittest
from tests_system.asserter import Asserter
from tests_system.lobster_report.lobster_report_system_test_case_base import (
    LobsterReportSystemTestCaseBase)


class ReportSchemaAndVersionTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_invalid_schema(self):
        # lobster-trace: core_report_req.Invalid_Schema
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_schema.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_schema.lobster")
        conf_file = "invalid_schema.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            f"is deprecated, please migrate to '.yaml' format\n"
            f"python_invalid_schema.lobster: "
            f"lobster error: unknown schema kind "
            f"invalid-schema-name\n\n"
            f"lobster-report: aborting due "
            f"to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_schema_yaml(self):
        # lobster-trace: core_report_req.Invalid_Schema
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_schema.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_schema.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_schema.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("python_invalid_schema.lobster: "
                                  "lobster error: unknown schema kind "
                                  "invalid-schema-name\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_missing_schema(self):
        # lobster-trace: core_report_req.Missing_Schema_Key
        self._test_runner.declare_input_file(
            self._data_directory / "missing_schema.conf")
        self._test_runner.declare_input_file(
            self._data_directory / "trlc_missing_schema.lobster")

        conf_file = "missing_schema.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            f"is deprecated, please migrate to '.yaml' format\n"
            f"trlc_missing_schema.lobster: "
            f"lobster error: required top-levelkey "
            f"schema not present\n\n"
            f"lobster-report: aborting due "
            f"to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_missing_schema_yaml(self):
        # lobster-trace: core_report_req.Missing_Schema_Key
        self._test_runner.declare_input_file(
            self._data_directory / "missing_schema.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "trlc_missing_schema.lobster")
        self._test_runner.cmd_args.lobster_config = "missing_schema.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_missing_schema.lobster: "
                                  "lobster error: required top-levelkey "
                                  "schema not present\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_invalid_version(self):
        # lobster-trace: core_report_req.Invalid_Schema_Version
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_version.conf")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_version.lobster")

        conf_file = "invalid_version.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            f"is deprecated, please migrate to '.yaml' format\n"
            f"python_invalid_version.lobster: "
            f"lobster error: version 99 for schema "
            f"lobster-req-trace is not supported\n\n"
            f"lobster-report: aborting due "
            f"to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_invalid_version_yaml(self):
        # lobster-trace: core_report_req.Invalid_Schema_Version
        self._test_runner.declare_input_file(self._data_directory /
                                             "invalid_version.yaml")
        self._test_runner.declare_input_file(self._data_directory /
                                             "trlc_zero_items.lobster")
        self._test_runner.declare_input_file(self._data_directory /
                                             "python_invalid_version.lobster")

        self._test_runner.cmd_args.lobster_config = "invalid_version.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("python_invalid_version.lobster: "
                                  "lobster error: version 99 for schema "
                                  "lobster-req-trace is not supported\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)

    def test_missing_version(self):
        # lobster-trace: core_report_req.Missing_Version_Key
        self._test_runner.declare_input_file(
            self._data_directory / "missing_version.conf")
        self._test_runner.declare_input_file(
            self._data_directory / "trlc_missing_version.lobster")

        conf_file = "missing_version.conf"
        self._test_runner.cmd_args.lobster_config = conf_file

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            f"{conf_file}: lobster warning: configuration file format '.conf' "
            f"is deprecated, please migrate to '.yaml' format\n"
            f"trlc_missing_version.lobster: "
            f"lobster error: required top-levelkey "
            f"version not present\n\n"
            f"lobster-report: aborting due "
            f"to earlier errors.\n"
        )
        asserter.assertExitCode(1)

    def test_missing_version_yaml_no_schema(self):
        # lobster-trace: core_report_req.Missing_Version_Key
        self._test_runner.declare_input_file(
            self._data_directory / "missing_version_no_schema.yaml")
        self._test_runner.declare_input_file(
            self._data_directory / "trlc_missing_version_no_schema.lobster")
        self._test_runner.cmd_args.lobster_config = "missing_version_no_schema.yaml"

        result = self._test_runner.run_tool_test()
        asserter = Asserter(self, result, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText("trlc_missing_version_no_schema.lobster: "
                                  "lobster error: required top-levelkey "
                                  "version not present\n\n"
                                  "lobster-report: aborting due "
                                  "to earlier errors.\n")
        asserter.assertExitCode(1)


if __name__ == "__main__":
    unittest.main()
