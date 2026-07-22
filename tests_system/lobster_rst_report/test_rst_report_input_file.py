import subprocess
import unittest
import unittest.mock

from lobster.common.graphviz_utils import is_dot_available
from lobster.common.location import File_Reference
from lobster.tools.core.rst_report._helpers import ItemNaming
from lobster.tools.core.rst_report.rst_report import _get_git_commit
from tests_system.asserter import Asserter
from tests_system.lobster_rst_report.lobster_rst_report_system_test_case_base import (
    LobsterRstReportSystemTestCaseBase,
)
from tests_system.tests_utils.update_version_in_rst_file import (
    update_version_in_rst_file,
)

_FIXED_COMMIT = "aaaa1111bbbb2222cccc3333dddd4444eeee5555"


class RstReportInputFileTest(LobsterRstReportSystemTestCaseBase):
    """Tests for input file handling by lobster-rst-report."""

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_missing_input_file_exits_nonzero(self):
        # lobster-trace: rst_req.Missing_Lobster_File
        self._test_runner.cmd_args.lobster_report = "does_not_exist.lobster"
        self._test_runner.cmd_args.out = "out.rst"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(2)
        asserter.assertInStdErr("does_not_exist.lobster")

    def test_malformed_lobster_file_exits_with_error(self):
        """A malformed .lobster file must cause a non-zero exit; the tool must
        not crash with an unhandled exception."""
        # Write a file that exists but contains invalid JSON.
        bad_file = self._test_runner.working_dir / "bad.lobster"
        bad_file.write_text("this is not valid json", encoding="UTF-8")
        self._test_runner.cmd_args.lobster_report = "bad.lobster"
        self._test_runner.cmd_args.out = "out.rst"

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(1)

    def test_valid_input_single_page_creates_rst_file(self):
        # lobster-trace: UseCases.RST_File_generation
        # lobster-trace: rst_req.Valid_Lobster_File
        # lobster-trace: rst_req.RST_Report_Single_Page
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_file = "report.rst"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out = out_file

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertNoStdErrText()

        output_path = self._test_runner.working_dir / out_file
        self.assertTrue(output_path.exists(), f"{out_file} was not created")

    def test_valid_input_single_page_rst_content(self):
        # lobster-trace: UseCases.RST_File_generation
        # lobster-trace: rst_req.Valid_Lobster_File
        # lobster-trace: rst_req.RST_Report_Coverage_Table
        # lobster-trace: rst_req.RST_Report_Issues_List
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_file = "report.rst"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out = out_file

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)

        output_path = self._test_runner.working_dir / out_file
        content = output_path.read_text(encoding="UTF-8")
        self.assertIn("L.O.B.S.T.E.R. Traceability Report", content)
        self.assertIn("Coverage Summary", content)
        self.assertIn("Issues", content)

    def test_valid_input_multi_page_creates_index_rst(self):
        # lobster-trace: rst_req.Valid_Lobster_File_Multi_Page
        # lobster-trace: rst_req.RST_Report_Multi_Page
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_dir = "rst_pages"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out_dir = out_dir

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertNoStdErrText()

        index_path = self._test_runner.working_dir / out_dir / "index.rst"
        self.assertTrue(index_path.exists(), "index.rst was not created")

    def test_valid_input_multi_page_creates_level_pages(self):
        # lobster-trace: rst_req.Valid_Lobster_File_Multi_Page
        # lobster-trace: rst_req.RST_Report_Multi_Page
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_dir = "rst_pages"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out_dir = out_dir

        completed_process = self._test_runner.run_tool_test()
        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)

        out_path = self._test_runner.working_dir / out_dir
        rst_files = list(out_path.glob("*.rst"))
        # Should have index.rst + at least one level page
        self.assertGreater(
            len(rst_files), 1, "Expected index.rst and at least one level page"
        )

    def _get_single_page_content(self) -> str:
        """Helper: run the tool and return the single-page RST content."""
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_file = "report.rst"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out = out_file
        completed_process = self._test_runner.run_tool_test()
        self.assertEqual(completed_process.returncode, 0)
        return (self._test_runner.working_dir / out_file).read_text(encoding="UTF-8")

    def test_tracing_policy_diagram_in_output(self):
        # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram
        # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram_Fallback
        content = self._get_single_page_content()
        if is_dot_available(dot=None):
            # dot is installed — the diagram is rendered as a Graphviz directive
            self.assertIn(".. graphviz::", content)
            self.assertIn("digraph tracing_policy", content)
        else:
            # dot is not installed — a fallback note is emitted instead
            self.assertIn(".. note::", content)
            self.assertIn("Tracing policy diagram omitted", content)

    def test_covered_requirements_listed(self):
        # lobster-trace: UseCases.RST_Covered_Requirement_list
        # lobster-trace: rst_req.RST_Report_Item_Details
        content = self._get_single_page_content()
        # A covered requirement with OK status (from System Requirements level)
        self.assertIn("[OK]", content)
        # A covered TRLC requirement that has OK status
        self.assertIn("example.req\\_implication", content)

    def test_not_covered_requirements_listed(self):
        # lobster-trace: UseCases.RST_Not_covered_Requirement_list
        content = self._get_single_page_content()
        # Missing TRLC requirements from the basic_report test data
        self.assertIn("[MISSING]", content)
        self.assertIn("example.req\\_xor", content)
        self.assertIn("example.req\\_nor", content)

    def test_tests_covering_requirements_listed(self):
        # lobster-trace: UseCases.RST_List_of_tests_covering_requirements
        content = self._get_single_page_content()
        # A GoogleTest item that is OK (has upward coverage)
        self.assertIn("ImplicationTest:BasicTest", content)

    def test_tests_not_covering_requirements_listed(self):
        # lobster-trace: UseCases.RST_List_of_tests_not_covering_requirements
        content = self._get_single_page_content()
        # Items with MISSING status at Code or Verification Test level
        # exclusive_or has MISSING status in the test data
        self.assertIn("exclusive\\_or", content)

    def test_coverage_values_in_output(self):
        # lobster-trace: UseCases.RST_Coverage_in_output
        # lobster-trace: rst_req.RST_Report_Coverage_Table
        content = self._get_single_page_content()
        # Software Requirements: 3/6 = 50.0%
        self.assertIn("50.0%", content)
        self.assertIn("3 of 6 items OK", content)
        # Code: 6/10 = 60.0%
        self.assertIn("60.0%", content)
        # System Requirements: 1/1 = 100.0%
        self.assertIn("100.0%", content)

    def test_findings_listed_in_output(self):
        # lobster-trace: UseCases.RST_Missing_tracing_policy_violation_in_output
        # lobster-trace: rst_req.RST_Report_Issues_List
        content = self._get_single_page_content()
        # Check that the issues list section appears
        self.assertIn("Issues", content)
        # The basic_report data has MISSING items — at least one must appear in the
        # issues list with a finding label
        self.assertIn("MISSING", content)

    def test_source_locations_in_output(self):
        # lobster-trace: UseCases.RST_Source_location_in_output
        # lobster-trace: UseCases.RST_Correct_Item_Data
        content = self._get_single_page_content()
        # Codebeamer URL for system requirement (item 666 on potato.kitten)
        self.assertIn("potato.kitten/issue/666", content)
        # GitHub URL for software requirements
        self.assertIn("github.com/bmw-software-engineering/lobster", content)
        # Links must be RST anonymous hyperlinks (not plain text)
        self.assertIn("`__", content)

    # ------------------------------------------------------------------
    # Multi-page content verification
    # ------------------------------------------------------------------

    def _get_multi_page_contents(self):
        """Helper: run the tool in multi-page mode and return a dict of
        {filename: content}."""
        self._test_runner = self.create_test_runner()
        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        out_dir = "rst_pages"
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out_dir = out_dir
        completed_process = self._test_runner.run_tool_test()
        self.assertEqual(completed_process.returncode, 0)
        out_path = self._test_runner.working_dir / out_dir
        pages = {}
        for rst_file in out_path.glob("*.rst"):
            pages[rst_file.name] = rst_file.read_text(encoding="UTF-8")
        return pages

    def test_multi_page_index_contains_toctree(self):
        # lobster-trace: rst_req.RST_Report_Multi_Page
        pages = self._get_multi_page_contents()
        index = pages["index.rst"]
        self.assertIn(".. toctree::", index)

    def test_multi_page_index_contains_doc_crossrefs(self):
        # lobster-trace: rst_req.RST_Report_Multi_Page
        # lobster-trace: rst_req.RST_Report_Coverage_Table
        pages = self._get_multi_page_contents()
        index = pages["index.rst"]
        # Multi-page mode uses :doc: links in the coverage table
        self.assertIn(":doc:", index)

    def test_multi_page_level_page_has_item_details(self):
        # lobster-trace: rst_req.RST_Report_Item_Details
        # lobster-trace: rst_req.RST_Report_Multi_Page
        pages = self._get_multi_page_contents()
        # Remove index.rst — the remaining files are level pages
        level_pages = {k: v for k, v in pages.items() if k != "index.rst"}
        self.assertGreater(len(level_pages), 0, "No level pages generated")
        # At least one level page must contain items (dropdown directives)
        any_items = any(".. dropdown::" in v for v in level_pages.values())
        self.assertTrue(any_items, "No items found in any level page")
        # At least one level page must show coverage
        any_coverage = any("Coverage:" in v for v in level_pages.values())
        self.assertTrue(any_coverage, "No coverage data in any level page")

    def test_codebeamer_link_rendered_in_output(self):
        # lobster-trace: UseCases.RST_Codebeamer_Links_In_Output
        # lobster-trace: rst_req.RST_Clickable_Codebeamer_Item
        content = self._get_single_page_content()
        # The basic_report.lobster has a codebeamer item at potato.kitten
        # with item 666 and version 42
        self.assertIn("potato.kitten/issue/666?version=42", content)
        # The link should be an RST anonymous hyperlink
        self.assertIn("`__", content)

    def test_codebeamer_item_name_displayed(self):
        # lobster-trace: rst_req.RST_Codebeamer_Item_Name
        content = self._get_single_page_content()
        # The codebeamer item in the test data has name "LOBSTER demo"
        self.assertIn("LOBSTER demo", content)


class RstReportGoldenOutputTest(LobsterRstReportSystemTestCaseBase):
    """Golden-file comparison tests for lobster-rst-report single-page output.

    Pattern mirrors tests_system/lobster_html_report/test_html_content.py:
    * Real ``is_dot_available(dot=None)`` call — no mocking of dot.
    * Two golden files, one per dot-availability state.
    * ``_get_git_commit`` is patched to a fixed hash so output is deterministic.
    * ``update_version_in_rst_file`` updates the LOBSTER version in the golden
      file copy before ``assertOutputFiles()`` compares it to the actual output.
    """

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_golden_single_page_output(self):
        # lobster-trace: UseCases.RST_File_generation
        # lobster-trace: rst_req.RST_Report_Single_Page
        # lobster-trace: rst_req.RST_Report_Header
        # lobster-trace: rst_req.RST_Report_Coverage_Table
        # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram
        # lobster-trace: rst_req.RST_Report_Tracing_Policy_Diagram_Fallback
        """Full single-page RST output matches the checked-in golden file."""
        if is_dot_available(dot=None):
            golden_name = "expected_single_page.rst"
        else:
            golden_name = "expected_single_page_no_dot.rst"

        expected_stdout_suffix = (
            (
                "warning: dot utility not found, report will not include "
                "the tracing policy visualisation\n"
                "> please install Graphviz (https://graphviz.org)\n"
            )
            if not is_dot_available(dot=None)
            else ""
        ) + f"LOBSTER RST report written to {golden_name}\n"

        golden_src = self._data_directory / golden_name

        # Copy the golden file into a separate temp dir so assertOutputFiles()
        # can compare it against the tool's actual output in working_dir.
        # (Both must share the same basename; they must be in different dirs.)
        output_dir = self.create_output_directory_and_copy_expected(
            self._data_directory.parent, golden_src
        )
        golden_copy = output_dir / golden_name
        update_version_in_rst_file(golden_copy)

        self._test_runner.declare_input_file(
            self._data_directory / "basic_report.lobster"
        )
        self._test_runner.declare_output_file(golden_copy)
        self._test_runner.cmd_args.lobster_report = "basic_report.lobster"
        self._test_runner.cmd_args.out = golden_name

        patch_target = (
            "lobster.tools.core.rst_report.rst_report._get_git_commit"
        )
        with unittest.mock.patch(patch_target, return_value=_FIXED_COMMIT):
            completed_process = self._test_runner.run_tool_test()

        asserter = Asserter(self, completed_process, self._test_runner)
        asserter.assertExitCode(0)
        asserter.assertStdOutText(expected_stdout_suffix)
        asserter.assertOutputFiles()


class GitCommitHelperTest(unittest.TestCase):
    """Unit tests for the ``_get_git_commit()`` report-header helper."""

    _RUN_TARGET = "lobster.tools.core.rst_report.rst_report.subprocess.run"

    def test_returns_stripped_commit_hash(self):
        # lobster-trace: rst_req.RST_Report_Header
        completed = subprocess.CompletedProcess(
            args=["git", "rev-parse", "HEAD"],
            returncode=0,
            stdout=f"{_FIXED_COMMIT}\n",
            stderr="",
        )
        with unittest.mock.patch(self._RUN_TARGET, return_value=completed):
            self.assertEqual(_get_git_commit(), _FIXED_COMMIT)

    def test_returns_unknown_when_git_not_installed(self):
        # lobster-trace: rst_req.RST_Report_Header
        with unittest.mock.patch(self._RUN_TARGET, side_effect=FileNotFoundError):
            self.assertEqual(_get_git_commit(), "(unknown)")

    def test_returns_unknown_outside_git_repository(self):
        # lobster-trace: rst_req.RST_Report_Header
        error = subprocess.CalledProcessError(128, ["git", "rev-parse", "HEAD"])
        with unittest.mock.patch(self._RUN_TARGET, side_effect=error):
            self.assertEqual(_get_git_commit(), "(unknown)")

    def test_returns_unknown_on_timeout(self):
        # lobster-trace: rst_req.RST_Report_Header
        error = subprocess.TimeoutExpired(["git", "rev-parse", "HEAD"], 5)
        with unittest.mock.patch(self._RUN_TARGET, side_effect=error):
            self.assertEqual(_get_git_commit(), "(unknown)")


class SourceRootNormalizationTest(unittest.TestCase):
    """Unit tests for ``--source-root`` trailing-slash normalization in links."""

    def test_source_root_without_trailing_slash_gets_one(self):
        # lobster-trace: rst_req.RST_Source_Root_Prefix
        link = ItemNaming.location_link(
            File_Reference("src/module/foo.cpp"), source_root="../.."
        )
        self.assertIn("<../../src/module/foo.cpp>", link)
        self.assertNotIn("..//", link)

    def test_source_root_with_trailing_slash_not_duplicated(self):
        # lobster-trace: rst_req.RST_Source_Root_Prefix
        link = ItemNaming.location_link(
            File_Reference("src/module/foo.cpp"), source_root="../../"
        )
        self.assertIn("<../../src/module/foo.cpp>", link)
        self.assertNotIn("..//", link)

    def test_no_source_root_uses_plain_filename(self):
        # lobster-trace: rst_req.RST_Source_Root_Prefix
        link = ItemNaming.location_link(
            File_Reference("src/module/foo.cpp"), source_root=""
        )
        self.assertIn("<src/module/foo.cpp>", link)


if __name__ == "__main__":
    unittest.main()
