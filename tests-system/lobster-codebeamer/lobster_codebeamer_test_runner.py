from subprocess import CompletedProcess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml
from ..test_runner import TestRunner


@dataclass
class ConfigFileData:
    import_query: Optional[bool] = None
    root: Optional[str] = None
    token: List[str] = None
    out: Optional[str] = None
    refs: Optional[List[str]] = None
    page_size: Optional[str] = None
    num_request_retry: Optional[bool] = None
    retry_error_codes: Optional[bool] = None

    def dump(self, filename: str):
        data = {}

        def append_if_not_none(key, value):
            if value is not None:
                data[key] = value

        append_if_not_none("import_query", self.import_query)
        append_if_not_none("root", self.root)
        append_if_not_none("token", self.token)
        append_if_not_none("out", self.out)
        append_if_not_none("refs", self.refs)
        append_if_not_none("page_size", self.page_size)
        append_if_not_none("num_request_retry", self.num_request_retry)
        append_if_not_none("retry_error_codes", self.retry_error_codes)

        with open(filename, mode='w', encoding="UTF-8") as file:
            yaml.dump(data, file)


@dataclass
class CmdArgs:
    out: Optional[str] = None
    config: Optional[str] = "config.yaml"

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        append_if_string("--out", self.out)
        append_if_string("--config", self.config)

        return cmd_args


class LobsterCodebeamerTestRunner(TestRunner):
    """System test runner for lobster-codebeamer"""

    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._config_file_data = ConfigFileData()
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    @property
    def config_file_data(self) -> ConfigFileData:
        return self._config_file_data

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to
        start 'lobster-codebeamer' under test"""
        return self._cmd_args.as_list()

    def run_tool_test(self) -> CompletedProcess:
        if self._cmd_args.config:
            self._config_file_data.dump(str(self._working_dir / self._cmd_args.config))
        return super().run_tool_test()
