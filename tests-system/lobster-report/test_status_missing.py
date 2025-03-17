from .run_report_tests import ReportTest


class ReportMissingTest(ReportTest):
    def test_status_missing(self):
        # lobster-trace: core_report_req.Status_Missing
        self._run_test(
            "lobster_missing.conf",
            "trlc_missing.lobster",
            "python_missing.lobster",
            "report_missing.lobster"
        )

    def test_status_missing_mixed(self):
        # lobster-trace: core_report_req.Status_Missing
        self._run_test(
            "lobster_mixed.conf",
            "trlc_mixed.lobster",
            "python_mixed.lobster",
            "report_mixed.lobster"
        )
