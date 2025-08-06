#!/usr/bin/env python3
#
# lobster_cpptest - Extract C++ tracing tags from comments in tests for LOBSTER
# Copyright (C) 2024-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from argparse import Namespace
import os.path
from copy import copy
from dataclasses import dataclass, field
from typing import List
from enum import Enum
import yaml
from lobster.exceptions import LOBSTER_Exception
from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.file_tag_generator import FileTagGenerator
from lobster.tools.cpptest.parser.constants import Constants
from lobster.tools.cpptest.parser.requirements_parser import \
    ParserForRequirements
from lobster.meta_data_tool_base import MetaDataToolBase

OUTPUT_FILE = "output_file"
CODEBEAMER_URL = "codebeamer_url"
KIND = "kind"
FILES = "files"
REQUIREMENTS = 'requirements'

NAMESPACE_CPP = "cpp"
FRAMEWORK_CPP_TEST = "cpptest"
KIND_FUNCTION = "Function"
CB_PREFIX = "CB-#"
MISSING = "Missing"
ORPHAN_TESTS = "OrphanTests"


class KindTypes(str, Enum):
    REQ = "req"
    ACT = "act"
    IMP = "imp"


@dataclass
class Config:
    codebeamer_url: str
    kind: KindTypes = KindTypes.REQ
    files: List[str] = field(default_factory=lambda: ["."])
    output_file: str = "report.lobster"


SUPPORTED_KINDS = [kind_type.value for kind_type in KindTypes]


def parse_config_file(file_name: str) -> Config:
    """
    Parse the configuration dictionary from the given YAML config file.

    The configuration dictionary for cpptest must contain `codebeamer_url`.
    It may also contain `kind`, `files`, and `output_file` keys.

    Parameters
    ----------
    file_name : str
        The file name of the cpptest YAML config file.

    Returns
    -------
    dict
        The dictionary containing the configuration for cpptest.

    Raises
    ------
    Exception
        If the config dictionary does not contain the required keys
        or is improperly formatted.
    """
    if not os.path.isfile(file_name):
        raise ValueError(f'{file_name} is not an existing file!')

    with open(file_name, "r", encoding='utf-8') as file:
        try:
            config_dict = yaml.safe_load(file)
        except yaml.scanner.ScannerError as ex:
            raise LOBSTER_Exception(message="Invalid config file") from ex

    if (not config_dict or
            CODEBEAMER_URL not in config_dict):
        raise ValueError(f'Please follow the right config file structure! '
                         f'Missing attribute {CODEBEAMER_URL}')

    codebeamer_url = config_dict.get(CODEBEAMER_URL)
    kind = config_dict.get(KIND, KindTypes.REQ.value)
    files = config_dict.get(FILES, ["."])
    output_file = config_dict.get(OUTPUT_FILE, "report.lobster")

    if not isinstance(output_file, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{OUTPUT_FILE} must be a string but got '
                         f'{type(output_file).__name__}.')

    if not isinstance(kind, str):
        raise ValueError(f'Please follow the right config file structure! '
                         f'{KIND} must be a string but got '
                         f'{type(kind).__name__}.')

    if kind not in SUPPORTED_KINDS:
        raise ValueError(f'Please follow the right config file structure! '
                         f'{KIND} must be one of '
                         f'{",".join(SUPPORTED_KINDS)} but got {kind}.')

    return Config(
        codebeamer_url=codebeamer_url,
        kind=kind,
        files=files if isinstance(files, list) else [files],
        output_file=output_file
    )


def get_test_file_list(file_dir_list: list, extension_list: list) -> list:
    """
    Gets the list of test files.

    Given file names are added to the test file list without
    validating against the extension list.
    From given directory names only file names will be added
    to the test file list if their extension matches against
    the extension list.

    Parameters
    ----------
    file_dir_list : list
        A list containing file names and/or directory names
        to parse for file names.
    extension_list : list
        The list of file name extensions.

    Returns
    -------
    list
        The list of test files

    Raises
    ------
    Exception
        If the config dict does not contain the required keys
        or contains not supported values.
    """
    test_file_list = []

    for file_dir_entry in file_dir_list:
        if os.path.isfile(file_dir_entry):
            test_file_list.append(file_dir_entry)
        elif os.path.isdir(file_dir_entry):
            for path, _, files in os.walk(file_dir_entry):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext in extension_list:
                        test_file_list.append(os.path.join(path, filename))
        else:
            raise ValueError(f'"{file_dir_entry}" is not a file or directory.')

    if len(test_file_list) == 0:
        raise ValueError(f'"{file_dir_list}" does not contain any test file.')

    return test_file_list


def collect_test_cases_from_test_files(test_file_list: list,
                                       codebeamer_url: str) -> list:
    """
    Collects the list of test cases from the given test files.

    Parameters
    ----------
    test_file_list : list
        The list of test files.
    codebeamer_url: str

    Returns
    -------
    list
        The list of test cases.
    """
    parser = ParserForRequirements()
    test_case_list = parser.collect_test_cases_for_test_files(
        test_files=test_file_list,
        codebeamer_url=codebeamer_url
    )
    return test_case_list


def create_lobster_items_output_dict_from_test_cases(
        test_case_list: list,
        config: Config) -> dict:
    """
    Creates the lobster items dictionary for the given test cases grouped by
    configured output.

    Parameters
    ----------
    test_case_list : list
        The list of test cases.
    config : Config
        The configuration setting.

    Returns
    -------
    dict
         The lobster items dictionary for the given test cases
         grouped by configured output.
    """

    output_file = config.output_file
    lobster_items_output_dict = {ORPHAN_TESTS: {}, output_file: {}}

    file_tag_generator = FileTagGenerator()
    for test_case in test_case_list:
        function_name: str = test_case.test_name
        file_name = os.path.abspath(test_case.file_name)
        line_nr = int(test_case.docu_start_line)
        function_uid = f"{file_tag_generator.get_tag(file_name)}" \
                       f":{function_name}:{line_nr}"
        tag = Tracing_Tag(NAMESPACE_CPP, function_uid)
        loc = File_Reference(file_name, line_nr)
        key = tag.key()

        activity = \
            Activity(
                tag=tag,
                location=loc,
                framework=FRAMEWORK_CPP_TEST,
                kind=KIND_FUNCTION
            )

        contains_no_tracing_target = True

        tracing_target_list = []
        tracing_target_kind = config.kind
        for test_case_marker_value in getattr(
                test_case,
                REQUIREMENTS
        ):
            if MISSING not in test_case_marker_value:
                test_case_marker_value = (
                    test_case_marker_value.replace(CB_PREFIX, ""))
                tracing_target = Tracing_Tag(
                    tracing_target_kind,
                    test_case_marker_value
                )
                tracing_target_list.append(tracing_target)

        if len(tracing_target_list) >= 1:
            contains_no_tracing_target = False
            lobster_item = copy(activity)
            for tracing_target in tracing_target_list:
                lobster_item.add_tracing_target(tracing_target)

            lobster_items_output_dict[output_file][key] = (
                lobster_item)

        if contains_no_tracing_target:
            lobster_items_output_dict.get(ORPHAN_TESTS)[key] = (
                activity)

    return lobster_items_output_dict


def write_lobster_items_output_dict(lobster_items_output_dict: dict):
    """
    Write the lobster items to the output.
    If the output file name is empty everything is written to stdout.

    Parameters
    ----------
    lobster_items_output_dict : dict
        The lobster items dictionary grouped by output.
    """
    lobster_generator = Constants.LOBSTER_GENERATOR
    orphan_test_items = lobster_items_output_dict.get(ORPHAN_TESTS, {})
    for output_file_name, lobster_items in lobster_items_output_dict.items():
        if output_file_name == ORPHAN_TESTS:
            continue

        lobster_items_dict: dict = copy(lobster_items)
        lobster_items_dict.update(orphan_test_items)
        item_count = len(lobster_items_dict)

        if output_file_name:
            with open(output_file_name, "w", encoding="UTF-8") as output_file:
                lobster_write(
                    output_file,
                    Activity,
                    lobster_generator,
                    lobster_items_dict.values()
                )
            print(f'Written {item_count} lobster items to '
                  f'"{output_file_name}".')


def lobster_cpptest(config: Config):
    """
    The main function to parse requirements from comments
    for the given list of files and/or directories and write the
    created lobster dictionary to the configured outputs.

    Parameters
    ----------
    config : Config
        The configuration setting
    """
    test_file_list = \
        get_test_file_list(
            file_dir_list=config.files,
            extension_list=[".cpp", ".cc", ".c", ".h"]
        )

    test_case_list = \
        collect_test_cases_from_test_files(
            test_file_list=test_file_list,
            codebeamer_url=config.codebeamer_url
        )

    lobster_items_output_dict: dict = \
        create_lobster_items_output_dict_from_test_cases(
            test_case_list=test_case_list,
            config=config
        )

    write_lobster_items_output_dict(
        lobster_items_output_dict=lobster_items_output_dict
    )


class CppTestTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="cpptest",
            description="Extract C++ tracing tags from comments in tests for LOBSTER",
            official=True,
        )
        self._argument_parser.add_argument(
            "--config",
            help=("Path to YAML file with arguments, "
                  "by default (cpptest-config.yaml)"),
            default="cpptest-config.yaml",
        )

    def _run_impl(self, options: Namespace) -> int:
        options = self._argument_parser.parse_args()

        try:
            config = parse_config_file(options.config)

            lobster_cpptest(
                config=config
            )

        except ValueError as exception:
            self._argument_parser.error(str(exception))

        return 0


def main() -> int:
    return CppTestTool().run()
