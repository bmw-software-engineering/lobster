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


class RequirementTypes(Enum):
    REQS = '@requirement'
    REQ_BY = '@required_by'
    DEFECT = '@defect'


LOBSTER_GENERATOR = "lobster_cpp_doxygen"
SUPPORTED_REQUIREMENTS = [RequirementTypes.REQS.value, RequirementTypes.REQ_BY.value,
                          RequirementTypes.DEFECT.value]
map_test_type_to_key_name = {
    RequirementTypes.REQS.value : 'requirements',
    RequirementTypes.REQ_BY.value : 'required_by',
    RequirementTypes.DEFECT.value: 'defect_tracking_ids',
}


def parse_cpp_config_file(file_name):
    assert isinstance(file_name, str)
    assert os.path.isfile(file_name)

    with open(file_name, "r") as file:
        config_data = json.loads(file.read())

    if not config_data.get(OUTPUT):
        raise Exception(f"Please follow the right structure of config "
                        f"file! missing attribute {OUTPUT}")

    output_files_data = list(config_data.get(OUTPUT).values())

    provided_markers = []
    for output_file_data in output_files_data:
        if not output_file_data.get(MARKERS) or not output_file_data.get(KIND):
            raise Exception(f"Please follow the right structure of config "
                            f"file! missing attributes {MARKERS} or {KIND}")
        provided_markers.append(output_file_data.get(MARKERS)[0])

    supported_references = set(SUPPORTED_REQUIREMENTS)

    if not set(provided_markers).issubset(supported_references):
        raise Exception("The provided requirement types are not supported! "
              "supported requirement types: '%s'" % ', '.join(SUPPORTED_REQUIREMENTS))

    return config_data.get(OUTPUT)


def get_test_file_list(file_dir_list, extension_list):
    file_list = []
    errors = []

    for file_dir_entry in file_dir_list:
        if os.path.isfile(file_dir_entry):
            file_list.append(file_dir_entry)
        elif os.path.isdir(file_dir_entry):
            for path, _, files in os.walk(file_dir_entry):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext in extension_list:
                        file_list.append(os.path.join(path, filename))
        else:
            errors.append(f'"{file_dir_entry}" is not a file or directory')

    if len(file_list) == 0:
        errors.append(f'"{file_dir_list}" does not contain any test file')

    return file_list, errors


def collect_test_cases_from_test_files(test_file_list) -> list:
    parser = ParserForRequirements()
    test_case_list = parser.collect_test_cases_for_test_files(test_files=test_file_list)
    return test_case_list


def create_lobster_implementations_dict_from_test_cases(test_case_list, markers_data) -> dict:
    prefix = os.getcwd()
    lobster_implementations_dict = {}

    for test_case in test_case_list:
        function_name: str = test_case.suite_name
        file_name = test_case.file_name
        line_nr = test_case.docu_start_line
        filename = os.path.relpath(file_name, prefix)
        line_nr = int(line_nr)
        function_uid = "%s:%s:%u" % (os.path.basename(filename),
                                     function_name,
                                     line_nr)
        tag = Tracing_Tag("cpp", function_uid)
        loc = File_Reference(filename, line_nr)
        kind = 'Function'

        if tag.key() not in lobster_implementations_dict:
            lobster_implementations_dict[tag.key()] = Implementation(
                tag=tag,
                location=loc,
                language="C/C++",
                kind=kind,
                name=function_name)
        for marker in markers_data.get(MARKERS):
            for test in getattr(test_case, map_test_type_to_key_name[marker]):
                if 'Missing' not in test:
                    test = test.replace("CB-#", "")
                    lobster_implementations_dict[tag.key()].add_tracing_target\
                        (Tracing_Tag(markers_data.get(KIND), test))

    return lobster_implementations_dict


def write_lobster_implementations_to_output(lobster_implementations_dict, output):
    if output:
        with open(output, "w", encoding="UTF-8") as output_file:
            lobster_write(output_file, Implementation, LOBSTER_GENERATOR, lobster_implementations_dict.values())
        item_count = len(lobster_implementations_dict)
        print(f'Written output for {item_count} items to {output}')

    else:
        lobster_write(sys.stdout, Implementation, LOBSTER_GENERATOR, lobster_implementations_dict.values())
        print()


def lobster_cpp_doxygen(file_dir_list, output_config):
    test_file_list, error_list = \
        get_test_file_list(
            file_dir_list=file_dir_list,
            extension_list=[".cpp", ".cc", ".c", ".h"]
        )

    if len(error_list) == 0:
        test_case_list = \
            collect_test_cases_from_test_files(
                test_file_list=test_file_list
        )
        for output, markers_data in output_config.items():
            lobster_implementations_dict: dict = \
                create_lobster_implementations_dict_from_test_cases(
                    test_case_list=test_case_list,
                    markers_data=markers_data
                )

            write_lobster_implementations_to_output(
                lobster_implementations_dict=lobster_implementations_dict,
                output=output)

    return error_list


def main():
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

    if options.config_file:
        if os.path.isfile(options.config_file):
            cpp_output_config = parse_cpp_config_file(options.config_file)
        else:
            ap.error("cannot open config file '%s'" % options.config_file)

    error_list = \
        lobster_cpp_doxygen(
            file_dir_list=options.files,
            output_config=cpp_output_config
        )

    for error in error_list:
        ap.error(error)


if __name__ == "__main__":
    sys.exit(main())