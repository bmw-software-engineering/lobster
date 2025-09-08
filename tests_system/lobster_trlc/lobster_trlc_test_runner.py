from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import yaml
from tests_system.testrunner import TestRunResult, TestRunner
from lobster.tools.trlc.trlc_tool import main


@dataclass
class ConfigFileData:
    inputs: Optional[List[str]] = None
    inputs_from_file: Optional[str] = None
    traverse_bazel_dirs : Optional[str] = None
    conversion_rules: Optional[List[dict]] = None
    to_string_rules: Optional[List[dict]] = None

    def __post_init__(self):
        self.inputs = []

    def dump(self, filename: str):
        data = {}

        def append_if_not_none(key, value):
            if value is not None:
                data[key] = value

        append_if_not_none("inputs", self.inputs)
        append_if_not_none("inputs-from-file", self.inputs_from_file)
        append_if_not_none("conversion-rules", self.conversion_rules)
        append_if_not_none("to-string-rules", self.to_string_rules)
        append_if_not_none("traverse-bazel-dirs", self.traverse_bazel_dirs)
        if self.traverse_bazel_dirs:
            raise NotImplementedError("Feature not yet implemented!")

        with open(filename, mode='w', encoding="UTF-8") as file:
            yaml.dump(data, file)


@dataclass
class CmdArgs:
    config: Optional[str] = None
    out: Optional[str] = None
    dir_or_files: Optional[List[str]] = None

    def as_list(self) -> List[str]:
        """Returns the command line arguments as a list"""
        cmd_args = []

        def append_if_string(parameter: str, value: Optional[str]):
            if value is not None:
                cmd_args.append(f"{parameter}={value}")

        append_if_string("--out", self.out)
        append_if_string("--config", self.config)
        if self.dir_or_files:
            cmd_args.extend(self.dir_or_files)
        return cmd_args


class LobsterTrlcTestRunner(TestRunner):
    """System test runner for lobster-TRLC"""
    def __init__(self, working_dir: Path, use_config_file_data: bool = True):
        super().__init__(main, working_dir)
        self.use_config_file_data = use_config_file_data
        if use_config_file_data:
            self._cmd_args = CmdArgs(config="config.yaml")
            self._config_file_data = ConfigFileData()
        else:
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

    def run_tool_test(self) -> TestRunResult:
        if self._cmd_args.config and self.use_config_file_data:
            self._config_file_data.dump(str(self._working_dir / self._cmd_args.config))
        return super().run_tool_test()
