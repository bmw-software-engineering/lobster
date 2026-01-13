from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from tests_system.testrunner import TestRunner
from lobster.tools.python.python import main


@dataclass
class CmdArgs:
    files: List[str]
    out: Optional[str] = None
    activity: bool = False
    single: bool = False
    only_tagged_functions: bool = False
    parse_decorator: Optional[List[str]] = None
    parse_versioned_decorator: Optional[List[str]] = None
    kind: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list for lobster-python"""
        cmd_args: List[str] = []

        if self.activity:
            cmd_args.append("--activity")
        if self.single:
            cmd_args.append("--single")
        if self.only_tagged_functions:
            cmd_args.append("--only-tagged-functions")
        if self.out is not None:
            cmd_args.append(f"--out={self.out}")
        if self.parse_decorator is not None:
            # Expect two elements: decorator and name_arg
            if len(self.parse_decorator) == 2:
                cmd_args.extend([
                    "--parse-decorator",
                    *self.parse_decorator,
                ])
        if self.parse_versioned_decorator is not None:
            # Expect three elements: decorator, name_arg, version_arg
            if len(self.parse_versioned_decorator) == 3:
                cmd_args.extend([
                    "--parse-versioned-decorator",
                    *self.parse_versioned_decorator,
                ])

        # Positional file/dir arguments come last
        if self.files:
            cmd_args.extend(self.files)
        if self.kind:
            cmd_args.extend(["--kind", self.kind])

        return cmd_args


class LobsterPythonTestRunner(TestRunner):
    """System test runner for lobster-python"""

    def __init__(self, working_dir: Path):
        super().__init__(main, working_dir)
        self._cmd_args = CmdArgs(files=[])

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments for 'lobster-python'"""
        return self._cmd_args.as_list()
