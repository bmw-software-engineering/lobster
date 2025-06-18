from subprocess import CompletedProcess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml
from ..test_runner import TestRunner


@dataclass
class ConfigFileData:
    single: Optional[bool] = None
    inputs: List[str] = None
    name_attribute: Optional[str] = None
    tag_attribute: Optional[str] = None
    justification_attribute: Optional[str] = None
    inputs_from_file: Optional[str] = None
    test_list: Optional[str] = None

    def __post_init__(self):
        self.inputs = []

    def dump(self, filename: str):
        data = {}

        def append_if_not_none(key, value):
            if value is not None:
                data[key] = value

        append_if_not_none("single", self.single)
        append_if_not_none("inputs", self.inputs)
        append_if_not_none("name_attribute", self.name_attribute)
        append_if_not_none("tag_attribute", self.tag_attribute)
        append_if_not_none("justification_attribute", self.justification_attribute)
        append_if_not_none("inputs_from_file", self.inputs_from_file)
        append_if_not_none("test_list", self.test_list)

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


class LobsterJsonTestRunner(TestRunner):
    """System test runner for lobster-json"""
    def __init__(self, tool_name: str, working_dir: Path):
        super().__init__(tool_name, working_dir)
        self._config_file_data = ConfigFileData(single=True)
        self._cmd_args = CmdArgs()

    @property
    def cmd_args(self) -> CmdArgs:
        return self._cmd_args

    @property
    def config_file_data(self) -> ConfigFileData:
        return self._config_file_data

    def declare_input_file(self, file: Path):
        super().declare_input_file(file)
        self.config_file_data.inputs.append(file.name)

    def declare_inputs_from_file(self, file, data_directory):
        super().declare_inputs_from_file(file, data_directory)
        self.config_file_data.inputs_from_file = file.name

    def get_tool_args(self) -> List[str]:
        """Returns the command line arguments that shall be used to start 'lobster-json'
           under test"""
        return self._cmd_args.as_list()

    def run_tool_test(self) -> CompletedProcess:
        if self._cmd_args.config:
            self._config_file_data.dump(str(self._working_dir / self._cmd_args.config))
        return super().run_tool_test()
