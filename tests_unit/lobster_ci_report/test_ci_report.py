import contextlib
import io
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import call, patch

from lobster.common.items import Requirement, Tracing_Status, Tracing_Tag
from lobster.common.location import File_Reference
from lobster.common.report import Coverage, Report
from lobster.tools.core.ci_report.ci_report import (
    CiReportTool,
    ensure_report_file_exists,
    format_coverage_lines,
    report_errors_for_untraced_items,
    resolve_report_path,
)


def make_item(status, messages):
    tag = Tracing_Tag("req", f"demo.{status.name.lower()}")
    item = Requirement(
        tag=tag,
        location=File_Reference("demo.trlc", 3, 5),
        framework="TRLC",
        kind="requirement",
        name=tag.tag,
    )
    item.tracing_status = status
    item.messages = messages
    return item


class ResolveReportPathTests(unittest.TestCase):

    def test_absolute_path_ignored_even_with_env_set(self):
        # lobster-trace: core_ci_report_req.Resolve_Report_Path_Uses_Build_Working_Directory
        with patch.dict(os.environ, {"BUILD_WORKING_DIRECTORY": "/other/dir"}):
            self.assertEqual(
                "/tmp/x/report.lobster",
                resolve_report_path("/tmp/x/report.lobster"),
            )

    def test_relative_path_resolved_against_build_working_directory(self):
        # lobster-trace: core_ci_report_req.Resolve_Report_Path_Uses_Build_Working_Directory
        with patch.dict(os.environ, {"BUILD_WORKING_DIRECTORY": "/some/dir"}):
            self.assertEqual(
                os.path.join("/some/dir", "report.lobster"),
                resolve_report_path("report.lobster"),
            )

    def test_relative_path_unchanged_without_env_var(self):
        # lobster-trace: core_ci_report_req.Resolve_Report_Path_Uses_Build_Working_Directory
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                "report.lobster",
                resolve_report_path("report.lobster"),
            )


class DefaultReportFileArgumentTests(unittest.TestCase):

    def test_default_value_is_report_lobster(self):
        # lobster-trace: core_ci_report_req.Default_Report_File_Argument
        # pylint: disable=protected-access
        argument_parser = CiReportTool()._argument_parser
        self.assertEqual(
            "report.lobster",
            argument_parser.get_default("lobster_report"),
        )


class EnsureReportFileExistsTests(unittest.TestCase):

    def setUp(self):
        # pylint: disable=protected-access
        self._parser = CiReportTool()._argument_parser

    def test_raises_on_missing_explicit_file(self):
        # lobster-trace: core_ci_report_req.Ensure_Report_File_Exists_Raises_On_Missing_File
        stderr = io.StringIO()
        with TemporaryDirectory() as tmp:
            resolved_path = str(Path(tmp) / "nonexistent.lobster")
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as ctx:
                    ensure_report_file_exists(
                        self._parser, "nonexistent.lobster", resolved_path,
                    )
        self.assertEqual(2, ctx.exception.code)
        self.assertIn("nonexistent.lobster is not a file", stderr.getvalue())

    def test_raises_on_missing_default_file(self):
        # lobster-trace: core_ci_report_req.Ensure_Report_File_Exists_Raises_On_Missing_File
        stderr = io.StringIO()
        with TemporaryDirectory() as tmp:
            resolved_path = str(Path(tmp) / "report.lobster")
            with contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as ctx:
                    ensure_report_file_exists(
                        self._parser, "report.lobster", resolved_path,
                    )
        self.assertEqual(2, ctx.exception.code)
        self.assertIn("specify report file", stderr.getvalue())

    def test_does_not_raise_when_file_exists(self):
        # lobster-trace: core_ci_report_req.Ensure_Report_File_Exists_Raises_On_Missing_File
        with TemporaryDirectory() as tmp:
            existing = Path(tmp) / "report.lobster"
            existing.write_text("{}", encoding="UTF-8")
            ensure_report_file_exists(self._parser, str(existing), str(existing))


class ReportErrorsForUntracedItemsTests(unittest.TestCase):

    def test_emits_error_for_each_message_of_untraced_items(self):
        # lobster-trace: core_ci_report_req.Report_Errors_For_Untraced_Items
        report = Report()
        ok_item = make_item(Tracing_Status.OK, [])
        missing_item = make_item(
            Tracing_Status.MISSING,
            ["missing up reference", "missing down reference"],
        )
        report.items[ok_item.tag.key()] = ok_item
        report.items[missing_item.tag.key()] = missing_item

        with patch.object(report.mh, "error") as mock_error:
            report_errors_for_untraced_items(report)

        mock_error.assert_has_calls([
            call(missing_item.location, "missing up reference", fatal=False),
            call(missing_item.location, "missing down reference", fatal=False),
        ])
        self.assertEqual(2, mock_error.call_count)

    def test_emits_nothing_for_fully_traced_items(self):
        # lobster-trace: core_ci_report_req.Report_Errors_For_Untraced_Items
        report = Report()
        ok_item = make_item(Tracing_Status.OK, [])
        justified_item = make_item(Tracing_Status.JUSTIFIED, [])
        report.items[ok_item.tag.key()] = ok_item
        report.items[justified_item.tag.key()] = justified_item

        with patch.object(report.mh, "error") as mock_error:
            report_errors_for_untraced_items(report)

        mock_error.assert_not_called()

    def test_emits_nothing_for_zero_items(self):
        # lobster-trace: core_ci_report_req.Report_Errors_For_Untraced_Items
        report = Report()

        with patch.object(report.mh, "error") as mock_error:
            report_errors_for_untraced_items(report)

        mock_error.assert_not_called()


class FormatCoverageLinesTests(unittest.TestCase):

    def test_formats_one_line_per_level(self):
        # lobster-trace: core_ci_report_req.Format_Coverage_Lines
        report = Report()
        report.coverage = {
            "Requirements": Coverage(level="Requirements", items=2, ok=1, coverage=50.0),
            "Tests": Coverage(level="Tests", items=3, ok=3, coverage=100.0),
        }
        self.assertEqual(
            [
                "coverage: Requirements: 50.0% (1 of 2 items)",
                "coverage: Tests: 100.0% (3 of 3 items)",
            ],
            format_coverage_lines(report),
        )


if __name__ == "__main__":
    unittest.main()
