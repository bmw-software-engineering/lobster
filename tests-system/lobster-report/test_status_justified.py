from .run_report_tests import ReportTest


class ReportJustifiedTest(ReportTest):
    def test_status_justified(self):
        # lobster-trace: core_report_req.Status_Justified_Global
        self._run_test(
            "lobster_justified.conf",
            "trlc_justified.lobster",
            "python_justified.lobster",
            "report_justified.lobster"
        )
