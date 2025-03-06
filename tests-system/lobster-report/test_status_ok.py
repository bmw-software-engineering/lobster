from os import makedirs
import shutil
from .lobsterreportsystemtestcasebase import LobsterReportSystemTestCaseBase
from .lobsterreportasserter import LobsterReportAsserter
from ..asserter import Asserter


class ReportOkTest(LobsterReportSystemTestCaseBase):
    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_status_ok(self):
        # lobster-trace: core_report_req.Status_Ok
        self._test_runner.declare_input_file(self._data_directory / "lobster.conf")
        self._test_runner.declare_input_file(self._data_directory / "trlc.lobster")
        self._test_runner.declare_input_file(self._data_directory / "python.lobster")

        out_file = "report.lobster"
        self._test_runner.cmd_args.out = out_file
        self._test_runner.declare_output_file(self._data_directory / out_file)

        completed_process = self._test_runner.run_tool_test()
        asserter = LobsterReportAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(0, out_file)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
