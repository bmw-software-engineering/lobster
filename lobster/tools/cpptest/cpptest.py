#!/usr/bin/env python3
#
# lobster_cpptest - Extract C++ tracing tags from comments in tests for LOBSTER
# Copyright (C) 2024 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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
from copy import copy
from enum import Enum

from lobster.items import Tracing_Tag, Activity
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.tools.cpptest.parser.constants import Constants
from lobster.tools.cpptest.parser.requirements_parser import \
    ParserForRequirements

OUTPUT  = "output"
CODEBEAMER_URL = "codebeamer_url"
MARKERS = "markers"
KIND    = "kind"

NAMESPACE_CPP = "cpp"
LANGUAGE_CPP = "C/C++"
FRAMEWORK_CPP_TEST = "cpptest"
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


def parse_config_file(file_name: str) -> dict:
    """
    Parse the configuration dictionary from given config file.

    The configuration dictionary for cpptest must contain the OUTPUT and
    CODEBEAMER_URL keys.
    Each output configuration dictionary contains a file name as key and
    a value dictionary containing the keys MARKERS and KIND.
    The supported values for the MARKERS list are specified in
    SUPPORTED_REQUIREMENTS.

    Parameters
    ----------
    file_name : str
        The file name of the cpptest config file.

    Returns
    -------
    dict
        The dictionary containing the configuration for cpptest.

    Raises
    ------
    Exception
        If the config dict does not contain the required keys
        or contains not supported values.
    """
    if not os.path.isfile(file_name):
        raise ValueError(f'{file_name} is not an existing file!')

    with open(file_name, "r", encoding='utf-8') as file:
        config_dict: dict = json.loads(file.read())

    if (OUTPUT not in config_dict.keys() or
            CODEBEAMER_URL not in config_dict.keys()):
        raise ValueError(f'Please follow the right config file structure! '
                         f'Missing attribute "{OUTPUT}" and '
                         f'"{CODEBEAMER_URL}"')

    output_config_dict = config_dict.get(OUTPUT)

    supported_markers = ', '.join(SUPPORTED_REQUIREMENTS)
    for output_file, output_file_config_dict in output_config_dict.items():
        if MARKERS not in output_file_config_dict.keys():
            raise ValueError(f'Please follow the right config file structure! '
                             f'Missing attribute "{MARKERS}" for output file '
                             f'"{output_file}"')
        if KIND not in output_file_config_dict.keys():
            raise ValueError(f'Please follow the right config file structure! '
                             f'Missing attribute "{KIND}" for output file '
                             f'"{output_file}"')

        output_file_marker_list = output_file_config_dict.get(MARKERS)
        for output_file_marker in output_file_marker_list:
            if output_file_marker not in SUPPORTED_REQUIREMENTS:
                raise ValueError(f'"{output_file_marker}" is not a supported '
                                 f'"{MARKERS}" value '
                                 f'for output file "{output_file}". '
                                 f'Supported values are: '
                                 f'"{supported_markers}"')

    return config_dict


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
        codebeamer_url = codebeamer_url
    )
    return test_case_list


def create_lobster_items_output_dict_from_test_cases(
        test_case_list: list,
        config_dict: dict) -> dict:
    """
    Creates the lobster items dictionary for the given test cases grouped by
    configured output.

    Parameters
    ----------
    test_case_list : list
        The list of test cases.
    config_dict : dict
        The configuration dictionary.

    Returns
    -------
    dict
         The lobster items dictionary for the given test cases
         grouped by configured output.
    """
    prefix = os.getcwd()
    lobster_items_output_dict = {}

    no_marker_output_file_name = ''
    output_config: dict = config_dict.get(OUTPUT)
    marker_output_config_dict = {}
    for output_file_name, output_config_dict in output_config.items():
        lobster_items_output_dict[output_file_name] = {}
        marker_list = output_config_dict.get(MARKERS)
        if isinstance(marker_list, list) and len(marker_list) >= 1:
            marker_output_config_dict[output_file_name] = output_config_dict
        else:
            no_marker_output_file_name = output_file_name

    if no_marker_output_file_name not in lobster_items_output_dict:
        lobster_items_output_dict[no_marker_output_file_name] = {}

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

        activity = \
            Activity(
                tag=tag,
                location=loc,
                framework=FRAMEWORK_CPP_TEST,
                kind=KIND_FUNCTION
            )

        contains_no_tracing_target = True
        for output_file_name, output_config_dict in (
                marker_output_config_dict.items()):
            tracing_target_list = []
            tracing_target_kind = output_config_dict.get(KIND)
            for marker in output_config_dict.get(MARKERS):
                if marker not in map_test_type_to_key_name:
                    continue

                for test_case_marker_value in getattr(
                        test_case,
                        map_test_type_to_key_name.get(marker)
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

                lobster_items_output_dict.get(output_file_name)[key] = (
                    lobster_item)

        if contains_no_tracing_target:
            lobster_items_output_dict.get(no_marker_output_file_name)[key] = (
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
    for output_file_name, lobster_items in lobster_items_output_dict.items():
        item_count = len(lobster_items)
        if item_count <= 1:
            continue

        if output_file_name:
            with open(output_file_name, "w", encoding="UTF-8") as output_file:
                lobster_write(
                    output_file,
                    Activity,
                    lobster_generator,
                    lobster_items.values()
                )
            print(f'Written {item_count} lobster items to '
                  f'"{output_file_name}".')

        else:
            lobster_write(
                sys.stdout,
                Activity,
                lobster_generator,
                lobster_items.values()
            )
            print(f'Written {item_count} lobster items to stdout.')


def lobster_cpptest(file_dir_list: list, config_dict: dict):
    """
    The main function to parse requirements from comments
    for the given list of files and/or directories and write the
    created lobster dictionary to the configured outputs.

    Parameters
    ----------
    file_dir_list : list
        The list of files and/or directories to be parsed
    config_dict : dict
        The configuration dictionary
    """
    test_file_list = \
        get_test_file_list(
            file_dir_list=file_dir_list,
            extension_list=[".cpp", ".cc", ".c", ".h"]
        )

    test_case_list = \
        collect_test_cases_from_test_files(
            test_file_list=test_file_list,
            codebeamer_url=config_dict.get(CODEBEAMER_URL, '')
        )

    lobster_items_output_dict: dict = \
        create_lobster_items_output_dict_from_test_cases(
            test_case_list=test_case_list,
            config_dict=config_dict
        )

    write_lobster_items_output_dict(
        lobster_items_output_dict=lobster_items_output_dict
    )


def main():
    """
    Main function to parse arguments, read configuration
    and launch lobster_cpptest.
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
        config_dict = parse_config_file(options.config_file)

        lobster_cpptest(
            file_dir_list=options.files,
            config_dict=config_dict
        )

    except ValueError as exception:
        ap.error(exception)


if __name__ == "__main__":
    sys.exit(main())
