from argparse import Namespace

from pathlib import Path
from typing import List
from tests_system.lobster_meta_data_tool_base.\
    lobster_meta_data_tool_base_cmd_args import CmdArgs
from tests_system.testrunner import TestRunner

from lobster.common.meta_data_tool_base import MetaDataToolBase


IMPLEMENTATION_MESSAGE = "This is the AppleBanana tool."


class LobsterMetaDataToolBaseTestRunner(TestRunner):
    """System test runner for abstract lobster base tool"""

    def __init__(self, working_dir: Path):
        def main(*args):
            class AppleBananaTool(MetaDataToolBase):
                def _run_impl(self, options: Namespace) -> int:
                    print(IMPLEMENTATION_MESSAGE)
                    return 0

            return AppleBananaTool(
                name="apple",
                description="banana",
                official=True,
            ).run(*args)

        super().__init__(main, working_dir)
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
