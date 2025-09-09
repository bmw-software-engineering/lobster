from tests_system.lobster_pkg.lobster_pkg_asserter import LobsterPkgAsserter
from tests_system.lobster_pkg.lobster_pkg_system_test_case_base import (
    LobsterPKGSystemTestCaseBase)
from pathlib import Path
import shutil


class InputFilePkgTest(LobsterPKGSystemTestCaseBase):

    def setUp(self):
        super().setUp()
        self._test_runner = self.create_test_runner()

    def test_valid_input_pkg_file(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Trace_in_Test_Step_Node
        # lobster-trace: req.Trace_in_Analysis_Node
        OUT_FILE = "valid_file1.lobster"
        self._test_runner.declare_input_file(self._data_directory / "valid_file1.pkg")
        self._test_runner.cmd_args.files = ["valid_file1.pkg"]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_input_ta_file(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Trace_in_Analysis_Node
        OUT_FILE = "valid_ta_file.lobster"
        self._test_runner.declare_input_file(self._data_directory / "valid_file.ta")
        self._test_runner.cmd_args.files = ["valid_file.ta"]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_ta_file_with_misplaced_traces(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: UseCases.Warning_for_Misplaced_Trace
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Misplaced_Traces
        OUT_FILE = "with_misplaced_traces.lobster"
        self._test_runner.cmd_args.files = [
            str(self._data_directory / "with_misplaced_traces.ta")
        ]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            'WARNING: misplaced lobster-trace in with_misplaced_traces.ta: '
            'lobster-trace:12345678\n'
            'WARNING: misplaced lobster-trace in with_misplaced_traces.ta: '
            'lobster-trace:98765432\n'
            'Written output for 1 items to with_misplaced_traces.lobster\n'
        )
        asserter.assertExitCode(0)

    def test_valid_pkg_file_with_misplaced_traces(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: UseCases.Warning_for_Misplaced_Trace
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Misplaced_Traces
        OUT_FILE = "valid_file1.lobster"
        self._test_runner.cmd_args.files = [
            str(self._data_directory / "with_misplaced_traces.pkg")
        ]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutText(
            'WARNING: misplaced lobster-trace in with_misplaced_traces.pkg: '
            'lobster-trace: misplaced.req1,misplaced.req2\n'
            'WARNING: misplaced lobster-trace in with_misplaced_traces.pkg: '
            'lobster-trace: misplaced.req3,misplaced.req4\n'
            'Written output for 1 items to valid_file1.lobster\n'
        )
        asserter.assertExitCode(0)

    def test_valid_input_pkg_files(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Trace_in_Test_Step_Node
        # lobster-trace: req.Trace_in_Analysis_Node
        OUT_FILE = "valid_file1_and_valid_file2.lobster"
        for file in ("valid_file1.pkg", "valid_file2.pkg"):
            self._test_runner.declare_input_file(self._data_directory / file)
            self._test_runner.cmd_args.files.append(file)

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(2, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_input_file_and_extra_file(self):
        """Test that an extra file in the working directory is ignored."""
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Trace_in_Test_Step_Node
        # lobster-trace: req.Trace_in_Analysis_Node
        OUT_FILE = "valid_file1.lobster"
        IN_FILES = ("valid_file1.pkg", "valid_file2.pkg")
        for f in IN_FILES:
            self._test_runner.copy_file_to_working_directory(self._data_directory / f)
        self._test_runner.cmd_args.files.append(IN_FILES[0])

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_input_pkg_folder(self):
        # lobster-trace: UseCases.PKG_Items_Extraction
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: req.Trace_in_Test_Step_Node
        # lobster-trace: req.Trace_in_Analysis_Node
        OUT_FILE = "valid_file1_folder.lobster"

        pkg_files_dir = Path(self._test_runner.working_dir) / "pkg_files"
        pkg_files_dir.mkdir(parents=True, exist_ok=True)

        src_pkg = self._data_directory / "valid_file1.pkg"
        dst_pkg = pkg_files_dir / "valid_file1.pkg"
        shutil.copy(src_pkg, dst_pkg)

        self._test_runner.cmd_args.files = ["pkg_files"]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)
        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)

        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_file_without_lobster_trace(self):
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: UseCases.PKG_Items_Extraction
        OUT_FILE = "without_lobster_trace.lobster"
        self._test_runner.declare_input_file(self._data_directory /
                                             "without_lobster_trace.pkg")
        self._test_runner.cmd_args.files = ["without_lobster_trace.pkg"]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()

    def test_valid_file_without_testcase_tag(self):
        # lobster-trace: req.Pkg_File_Item
        # lobster-trace: UseCases.PKG_Items_Extraction
        OUT_FILE = "without_testcase_tag.lobster"
        self._test_runner.declare_input_file(self._data_directory /
                                             "without_testcase_tag.pkg")
        self._test_runner.cmd_args.files = ["without_testcase_tag.pkg"]

        self._test_runner.cmd_args.out = OUT_FILE
        completed_process = self._test_runner.run_tool_test()

        out_file = self._data_directory / OUT_FILE
        self._test_runner.declare_output_file(out_file)

        asserter = LobsterPkgAsserter(self, completed_process, self._test_runner)
        asserter.assertNoStdErrText()
        asserter.assertStdOutNumAndFile(1, OUT_FILE)
        asserter.assertExitCode(0)
        asserter.assertOutputFiles()
