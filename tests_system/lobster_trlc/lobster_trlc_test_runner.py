from subprocess import CompletedProcess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml
from ..test_runner import TestRunner


class LiteralString(str):
    pass


@dataclass
class ConfigFileData:
    inputs: List[str] = None
    trlc_config : Optional[LiteralString] = None
    inputs_from_file: Optional[str] = None
    traverse_bazel_dirs : Optional[str] = None

    def __post_init__(self):
        self.inputs = []

    def dump(self, filename: str):
        data = {}

        def append_if_not_none(key, value):
            if value is not None:
                data[key] = value

        def literal_representer(dumper, data):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

        yaml.add_representer(LiteralString, literal_representer)

        append_if_not_none("inputs", self.inputs)
        append_if_not_none("inputs_from_file", self.inputs_from_file)
        append_if_not_none("trlc_config", self.trlc_config)
        append_if_not_none("traverse_bazel_dirs", self.traverse_bazel_dirs)

        with open(filename, mode='w', encoding="UTF-8") as file:
            yaml.dump(data, file)


@dataclass
class CmdArgs:
    config: Optional[str] = "config.yaml"
    out: Optional[str] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        append_if_string("--out", self.out)
        append_if_string("--config", self.config)
        return cmd_args


class LobsterTrlcTestRunner(TestRunner):
    """System test runner for lobster-TRLC"""
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

    def copy_files_in_working_directory(self, files: List):
        for file_path in files:
            super().declare_input_file(file_path)

    def declare_input_file(self, file: Path):
        super().declare_input_file(file)
        self.config_file_data.inputs.append(file.name)

    def read_config_from_file(self, file: Path) -> str:
        config_string = ""
        with open(file, "r", encoding="UTF-8") as fd:
            config_string = fd.read()

        return config_string

    def declare_trlc_config(self, trlc_config: str):
        self.config_file_data.trlc_config = LiteralString(trlc_config)

    def declare_inputs_from_file(self, file: Path, data_directory: Path):
        super().declare_input_file(file)
        self.config_file_data.inputs_from_file = file.name
        # TODO
        #  This will only work for files and not for directories.
        #  Traversing directories logic needs to be added
        with open(file, "r", encoding="UTF-8") as fd:
            for line in fd:
                super().declare_input_file(data_directory / line.strip())

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start 'lobster-trlc'
           under test"""
        return self._cmd_args.as_list()

    def run_tool_test(self) -> CompletedProcess:
        if self._cmd_args.config:
            self._config_file_data.dump(str(self._working_dir / self._cmd_args.config))
        return super().run_tool_test()
