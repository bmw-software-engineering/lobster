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

import sys
import argparse
import os.path

from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference
from lobster.io import lobster_write
from lobster.tools.cpp_doxygen.parser.requirements_parser import ParserForRequirements


LOBSTER_GENERATOR = "lobster_cpp_doxygen"


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


def create_lobster_implementations_dict_from_test_cases(test_case_list) -> dict:
    prefix = os.getcwd()
    lobster_implementations_dict = {}

    for test_case in test_case_list:
        # get requirement detail properties from test_case
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

        for requirement in test_case.requirements:
            if 'Missing' not in requirement:
                requirement = requirement.replace("CB-#", "")
                lobster_implementations_dict[tag.key()].add_tracing_target(Tracing_Tag("req", requirement))

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


def lobster_cpp_doxygen(file_dir_list, output):
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

        lobster_implementations_dict: dict = \
            create_lobster_implementations_dict_from_test_cases(
                test_case_list=test_case_list
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
    ap.add_argument("--out",
                    default=None,
                    help="write output to this file; otherwise output to stdout")

    options = ap.parse_args()
    error_list = \
        lobster_cpp_doxygen(
            file_dir_list=options.files,
            output=options.out
        )

    for error in error_list:
        ap.error(error)


if __name__ == "__main__":
    sys.exit(main())
