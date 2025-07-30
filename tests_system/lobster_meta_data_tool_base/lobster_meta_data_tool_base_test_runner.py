from pathlib import Path
from typing import List
from .lobster_meta_data_tool_base_cmd_args import CmdArgs
from ..test_runner import TestRunner


class LobsterMetaDataToolBaseTestRunner(TestRunner):
    """System test runner for abstract lobster base tool"""

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._cmd_args = CmdArgs()

    @staticmethod
    def _get_module_path(filename: str) -> str:
        """Returns the module path for the given filename

           The module path is the same as the relative path from the repository root
           to the file, but with dots instead of slashes and without the ".py" suffix.
        """
        path = (Path(__file__).parent / filename).resolve()
        rel_path = path.relative_to(path.parents[2].resolve())
        return ".".join(rel_path.with_suffix("").parts)

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start
        'lobster-tool-base' under test"""
        return self._cmd_args.as_list()
