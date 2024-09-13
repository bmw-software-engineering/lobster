#!/usr/bin/env python3
#
# lobster_cpp_doxygen - Extract C/C++ tracing tags from doxygen commands for LOBSTER
# Copyright (C) 2023 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import json
import sys
import argparse
import os.path
from enum import Enum

from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.tools.cpp_doxygen.parser.constants import LOBSTER_GENERATOR
from lobster.tools.cpp_doxygen.parser.requirements_parser import ParserForRequirements

OUTPUT  = "output"
MARKERS = "markers"
KIND    = "kind"

NAMESPACE_CPP = "cpp"
LANGUAGE_CPP = "C/C++"
KIND_FUNCTION = "Function"
CB_PREFIX = "CB-#"
MISSING = "Missing"


class RequirementTypes(Enum):
    REQS = '@requirement'
    REQ_BY = '@requiredby'
    DEFECT = '@defect'


SUPPORTED_REQUIREMENTS = [
    RequirementTypes.REQS.value,
    RequirementTypes.REQ_BY.value,
    RequirementTypes.DEFECT.value
]

map_test_type_to_key_name = {
    RequirementTypes.REQS.value: 'requirements',
    RequirementTypes.REQ_BY.value: 'required_by',
    RequirementTypes.DEFECT.value: 'defect_tracking_ids',
}


def parse_cpp_doxygen_config_file(file_name: str) -> dict:
    """
    Parse the configuration dictionary for cpp_doxygen from given config file.

    The configuration dictionary for cpp_doxygen must contain the OUTPUT key.
    Each output configuration dictionary contains a file name as key and
    a value dictionary containing the keys MARKERS and KIND.
    The supported values for the MARKERS list are specified in SUPPORTED_REQUIREMENTS.

    Parameters
    ----------
    file_name : str
        The file name of the cpp_doxygen config file.

    Returns
    -------
    dict
        The dictionary containing the configuration for cpp_doxygen.

    Raises
    ------
    Exception
        If the config dict does not contain the required keys
        or contains not supported values.
    """
    if not os.path.isfile(file_name):
        raise Exception(f'{file_name} is not an existing file!')

    with open(file_name, "r") as file:
        config_dict: dict = json.loads(file.read())

    if OUTPUT not in config_dict.keys():
        raise Exception(f'Please follow the right config file structure! '
                        f'Missing attribute "{OUTPUT}"')

    output_config_dict = config_dict.get(OUTPUT)

    supported_markers = ', '.join(SUPPORTED_REQUIREMENTS)
    for output_file, output_file_config_dict in output_config_dict.items():
        if MARKERS not in output_file_config_dict.keys():
            raise Exception(f'Please follow the right config file structure! '
                            f'Missing attribute "{MARKERS}" for output file "{output_file}"')
        if KIND not in output_file_config_dict.keys():
            raise Exception(f'Please follow the right config file structure! '
                            f'Missing attribute "{KIND}" for output file "{output_file}"')

        output_file_marker_list = output_file_config_dict.get(MARKERS)
        for output_file_marker in output_file_marker_list:
            if output_file_marker not in SUPPORTED_REQUIREMENTS:
                raise Exception(f'"{output_file_marker}" is not a supported "{MARKERS}" value '
                                f'for output file "{output_file}". '
                                f'Supported values are: "{supported_markers}"')

    return config_dict


def get_test_file_list(file_dir_list: list, extension_list: list) -> list:
    """
    Gets the list of test files.

    Given file names are added to the test file list without validating against the extension list.
    From given directory names only file names will be added to the test file list if their extension matches
    against the extension list.

    Parameters
    ----------
    file_dir_list : list
        A list containing file names and/or directory names to parse for file names.
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
            raise Exception(f'"{file_dir_entry}" is not a file or directory.')

    if len(test_file_list) == 0:
        raise Exception(f'"{file_dir_list}" does not contain any test file.')

    return test_file_list


def collect_test_cases_from_test_files(test_file_list: list) -> list:
    """
    Collects the list of test cases from the given test files.

    Parameters
    ----------
    test_file_list : list
        The list of test files.

    Returns
    -------
    list
        The list of test cases.
    """
    parser = ParserForRequirements()
    test_case_list = parser.collect_test_cases_for_test_files(test_files=test_file_list)
    return test_case_list


def create_lobster_implementations_dict_from_test_cases(test_case_list: list, config_dict: dict) -> dict:
    """
    Creates the lobster implementations dictionary for the given test cases.

    Parameters
    ----------
    test_case_list : list
        The list of test cases.
    config_dict : dict
        The configuration dictionary containing MARKERS and KIND values.

    Returns
    -------
    dict
        Dictionary containing the lobster implementations for all test cases.
    """
    prefix = os.getcwd()
    lobster_implementations_dict = {}
    lobster_implementations_reduced_dict = {}
    implementation_with_tracing_target = []

    for test_case in test_case_list:
        function_name: str = test_case.suite_name
        file_name = os.path.relpath(test_case.file_name, prefix)
        line_nr = int(test_case.docu_start_line)
        function_uid = "%s:%s:%u" % (os.path.basename(file_name),
                                     function_name,
                                     line_nr)
        tag = Tracing_Tag(NAMESPACE_CPP, function_uid)
        loc = File_Reference(file_name, line_nr)
        key = tag.key()

        if key not in lobster_implementations_dict.keys():
            lobster_implementations_dict[key] = \
                Implementation(
                    tag=tag,
                    location=loc,
                    language=LANGUAGE_CPP,
                    kind=KIND_FUNCTION,
                    name=function_name
                )

        for marker in config_dict.get(MARKERS):
            if marker not in map_test_type_to_key_name.keys():
                continue

            for test_case_marker_value in getattr(test_case, map_test_type_to_key_name.get(marker)):
                if MISSING not in test_case_marker_value:
                    test_case_marker_value = test_case_marker_value.replace(CB_PREFIX, "")
                    tracing_target = Tracing_Tag(config_dict.get(KIND), test_case_marker_value)
                    lobster_implementations_dict.get(key).add_tracing_target(tracing_target)
                    if key not in implementation_with_tracing_target:
                        implementation_with_tracing_target.append(key)

    for key, lobster_implementation in lobster_implementations_dict.items():
        if key in implementation_with_tracing_target:
            lobster_implementations_reduced_dict[key] = lobster_implementation

    return lobster_implementations_reduced_dict


def write_lobster_implementations_to_output(lobster_implementations_dict: dict, output_file_name: str):
    """
    Write the lobster implementations dictionary to the configured output.
    If the output file name is empty everything is written to stdout.

    Parameters
    ----------
    lobster_implementations_dict : dict
        The dictionary containing the lobster implementations.
    output_file_name : str
        The output file name.
    """
    if output_file_name:
        with open(output_file_name, "w", encoding="UTF-8") as output_file:
            lobster_write(output_file, Implementation, LOBSTER_GENERATOR, lobster_implementations_dict.values())
        item_count = len(lobster_implementations_dict)
        print(f'Written output for {item_count} items to {output_file_name}')

    else:
        lobster_write(sys.stdout, Implementation, LOBSTER_GENERATOR, lobster_implementations_dict.values())
        print()


def lobster_cpp_doxygen(file_dir_list: list, output_config: dict):
    """
    The main function to parse requirements from cpp doxygen comments
    for the given list of files and/or directories and write the
    created lobster implementations dictionary to the configured outputs.

    Parameters
    ----------
    file_dir_list : list
        The list of files and/or directories to be parsed
    output_config : dict
        The output configuration dictionary
    """
    test_file_list = \
        get_test_file_list(
            file_dir_list=file_dir_list,
            extension_list=[".cpp", ".cc", ".c", ".h"]
        )

    test_case_list = \
        collect_test_cases_from_test_files(
            test_file_list=test_file_list
        )

    for output_file_name, output_config_dict in output_config.items():
        lobster_implementations_dict: dict = \
            create_lobster_implementations_dict_from_test_cases(
                test_case_list=test_case_list,
                config_dict=output_config_dict
            )

        write_lobster_implementations_to_output(
            lobster_implementations_dict=lobster_implementations_dict,
            output_file_name=output_file_name)


def main():
    """
    Main function to parse arguments, read cpp doxygen configuration and launch
    lobster_cpp_doxygen.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("files",
                    nargs="+",
                    metavar="FILE|DIR")
    ap.add_argument("--config-file",
                    help="path of the config file, it consists of "
                         "a requirement types as keys and "
                         "output filenames as value",
                    required=True,
                    default=None)

    options = ap.parse_args()

    try:
        cpp_doxygen_config = parse_cpp_doxygen_config_file(options.config_file)

        lobster_cpp_doxygen(
            file_dir_list=options.files,
            output_config=cpp_doxygen_config.get(OUTPUT)
        )

    except Exception as exception:
        ap.error(exception)


if __name__ == "__main__":
    sys.exit(main())
