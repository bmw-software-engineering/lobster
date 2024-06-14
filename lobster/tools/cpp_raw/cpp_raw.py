#!/usr/bin/env python3
#
# lobster_cpp_raw - Extract C/C++ tracing tags for LOBSTER
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

import os.path
import re
import sys

from argparse import ArgumentParser, Namespace
from io import TextIOWrapper
from typing import Callable, Dict, List, Tuple
from lobster.io import lobster_write
from lobster.items import Tracing_Tag, Implementation
from lobster.location import File_Reference


class MisplacedTagException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CppRawArgumentParser(ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.add_argument("files",
                          nargs="+",
                          metavar="FILE|DIR")
        self.add_argument("--only-tagged-functions",
                          default=False,
                          action="store_true",
                          help="only trace functions with tags")
        self.add_argument("--out",
                          default=None,
                          help=("write output to this file; otherwise output "
                                "to to stdout"))


def get_valid_files(file_dir: List[str],
                    argument_parser: CppRawArgumentParser) -> List[str]:
    file_list = []
    for item in file_dir:
        if os.path.isfile(item):
            file_list.append(item)
        elif os.path.isdir(item):
            for path, _, files in os.walk(item):
                for filename in files:
                    _, ext = os.path.splitext(filename)
                    if ext in (".cpp", ".cc", ".c", ".h"):
                        file_list.append(os.path.join(path, filename))
        else:
            argument_parser.error("%s is not a file or directory" % item)
    return file_list


def extract_function_name(all_lines: List[str], trace_line: int) -> str:
    if trace_line < len(all_lines):
        function_name_match = re.search(r'\b(\w+)\(',
                                        all_lines[trace_line + 1])
        if function_name_match:
            return function_name_match.group(1)
        else:
            return None


def write_to_file(options: Namespace, data: Dict[str, Implementation]) -> None:
    with open(options.out, "w", encoding="UTF-8") as file:
        lobster_write(file, Implementation, "lobster-cpp_raw", data.values())
        print("Written output for %u items to %s" % (len(data), options.out))


def find_lobster_traces(all_lines: List[str]) -> List[Tuple[List[str], int]]:
    matches = []
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        match = re.search(r'lobster-trace:\s*(.*)', line)
        if match:
            items = match.group(1).split(',')
            matches.append(([item.strip() for item in items], i))
        i += 1
    return matches


def find_lobster_excludes(all_lines: List[str]) -> List[Tuple[re.Match, int]]:
    matches = []
    i = 0
    while i < len(all_lines):
        line = all_lines[i]
        match = re.search(r'lobster-exclude:\s*(.*)', line)
        if match:
            matches.append((match, i))
        i += 1
    return matches


def find_all_function_decl(file_content: str) -> List[Tuple[re.Match, int]]:
    function_matches = []
    matches = re.finditer(r'(\w+)\s*\([^;]*\)\s*\{', file_content)
    for match in matches:
        start_pos = match.start()
        line_number = file_content.count('\n', 0, start_pos) + 1
        function_matches.append((match, line_number))
    return function_matches


def create_raw_entry(data: Dict[str, Implementation], file_name: str,
                     name: str, line_number: int) -> Tracing_Tag:
    tag = Tracing_Tag("cpp", f"{file_name}:{name}:{line_number}")
    loc = File_Reference(file_name, line_number)
    data[tag.key()] = Implementation(
        tag      = tag,
        location = loc,
        language = "C/C++",
        kind     = "function",
        name     = name)
    return tag


def create_entry(match: Tuple[List[str], int],
                 data: Dict[str, Implementation],
                 all_lines: List[str], file: TextIOWrapper,
                 tag_type: str) -> Tracing_Tag:
    line = match[1]
    function_line = line + 1
    name = extract_function_name(all_lines, line)
    if name is None:
        raise MisplacedTagException("ERROR: No function declaration "
                                    "found following the "
                                    f"'{tag_type}' in line {line + 1}")
    return create_raw_entry(data, file.name, name, function_line + 1)


def create_trace_entry(match: Tuple[List[str], int],
                       data: Dict[str, Implementation],
                       all_lines: List[str], file: TextIOWrapper) -> None:
    tag = create_entry(match, data, all_lines, file, "lobster-trace")
    for req in match[0]:
        data[tag.key()].add_tracing_target(Tracing_Tag("req", req))


def create_exclude_entry(match: Tuple[re.Match, int],
                         data: Dict[str, Implementation],
                         all_lines: List[str], file: TextIOWrapper) -> None:
    tag = create_entry(match, data, all_lines, file, "lobster-exclude")
    data[tag.key()].just_up.append(match[0].group(1))


def create_remaining_function_decl(data: Dict[str, Implementation],
                                   file_content: str,
                                   file: TextIOWrapper) -> None:
    function_matches = find_all_function_decl(file_content)
    for match in function_matches:
        create_raw_entry(data, file.name, match[0].group(1), match[1])


def create_lobster_entries(data: Dict[str, Implementation],
                           all_lines: List[str],
                           file: TextIOWrapper, find_function: Callable,
                           create_type_entry: Callable) -> List[int]:
    tracing_matches = find_function(all_lines)
    lines_of_creation = []
    for match in tracing_matches:
        lines_of_creation.append(match[1])
        create_type_entry(match, data, all_lines, file)
    return lines_of_creation


def main() -> int:
    argument_parser = CppRawArgumentParser()
    options = argument_parser.parse_args()
    file_list = get_valid_files(options.files, argument_parser)
    data = {}

    for file_path in file_list:
        with open(file_path, 'r', encoding="UTF-8") as file:
            file_content = file.read()
            all_lines = file_content.split('\n')
            try:
                lines_to_remove = create_lobster_entries(data, all_lines, file,
                                                         find_lobster_traces,
                                                         create_trace_entry)
                if options.only_tagged_functions:
                    continue
                lines_to_remove.extend(
                    create_lobster_entries(data, all_lines, file,
                                           find_lobster_excludes,
                                           create_exclude_entry))
                for line in lines_to_remove:
                    all_lines[line] = ""
                    all_lines[line + 1] = ""
                remaining_content = '\n'.join(all_lines)
                create_remaining_function_decl(data, remaining_content, file)
            except MisplacedTagException as e:
                print(f"{e}\nERROR: Misplaced LOBSTER tag "
                      f"in file {file.name}")
                return 1

    if options.out:
        write_to_file(options, data)
    else:
        lobster_write(sys.stdout, Implementation, "lobster-cpp_raw",
                      data.values())
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
