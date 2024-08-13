# Copyright (C) 2020, Bayerische Motoren Werke Aktiengesellschaft (BMW AG)

import os
import re
import sys
from lobster.tools.cpp_parser.parser.tracing.tracing_regex import regex_trace_comp_tag, regex_test_pattern


def get_absolute_file_path(the_file):
    abs_path = os.path.abspath(the_file)
    return abs_path


def read_list_of_test_files_from_tracing_aspect_file_names(tracing_aspect_file_names):
    test_files = []
    for tracing_aspect_file_name in tracing_aspect_file_names:
        if not ".tracing.out" in tracing_aspect_file_name:
            continue
        with open(tracing_aspect_file_name) as tracing_aspect_file:
            for line in tracing_aspect_file.readlines():
                test_files.extend(line.split())
    return test_files


def check_regex_in_comment_section(comment_style, end_index, lines, is_triple_slash_comment=True):
    for index in range(end_index, 0, -1):
        if regex_trace_comp_tag.search(lines[index]):
            return True
        else:
            if index > 1 and (
                (is_triple_slash_comment and comment_style in lines[index - 1])
                or (comment_style not in lines[index - 1])
            ):
                continue
            else:
                break
    return False


def check_for_requirement(index, lines):
    triple_slash_comment = "///"
    slash_star_comment_open = "/*"
    slash_star_comment_close = "*/"
    for end_index in range(index, 0, -1):
        if triple_slash_comment in lines[end_index]:
            return check_regex_in_comment_section(triple_slash_comment, end_index, lines)
        elif slash_star_comment_close in lines[end_index]:
            return check_regex_in_comment_section(slash_star_comment_open, end_index, lines, False)
        elif not lines[end_index]:
            continue
        break
    return False


def check_for_component_tracibility(file):
    is_traced_component_test = False
    with open(file, "r") as the_file:
        lines = the_file.readlines()
        for index, _ in enumerate(lines):
            if not re.findall(regex_test_pattern, lines[index]):
                continue
            if check_for_requirement(index - 1, lines):
                is_traced_component_test = True
                break
    return is_traced_component_test


def get_traced_component_tests(component_test_files):
    test_files = []
    for test_file in component_test_files:
        if check_for_component_tracibility(test_file):
            test_files.append(test_file)
    return test_files
