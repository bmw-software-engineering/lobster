from .run_report_tests import ReportTest


class ReportOkTest(ReportTest):
    def test_status_missing_ok(self):
        # lobster-trace: core_report_req.Status_Ok
        self._run_test(
            "lobster_ok.conf",
            "trlc_ok.lobster",
            "python_ok.lobster",
            "report_ok.lobster"
        )
