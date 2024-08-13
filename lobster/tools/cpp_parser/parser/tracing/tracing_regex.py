# Copyright (C) 2020, Bayerische Motoren Werke Aktiengesellschaft (BMW AG)

import re

regex_test_pattern = r"^(TEST|TEST_P|TEST_F|TEST_P_INSTANCE|TEST_F_INSTANCE|TYPED_TEST|TYPED_TEST_P)(\(\s*)(?P<suite_name>[A-Za-z0-9_]*)(,\s*)(?P<test_name>[A-Za-z0-9_]*)(\))"

BENCHMARK_ONE_PARAMETER_PATTERN = r"^(BENCHMARK)(\(\s*)(?P<benchmark1_para1>\w*)(\))"

BENCHMARK_TWO_PARAMETERS_PATTERN = (
    r"^(BENCHMARK_DEFINE_F|BENCHMARK_F)(\(\s*)(?P<benchmark2_para1>\w*)(,\s*)(?P<benchmark2_para2>\w*)(\))"
)

BENCHMARK_THREE_PARAMETERS_PATTERN = r"^(BENCHMARK_TEMPLATE_F|BENCHMARK_CAPTURE|BENCHMARK_TEMPLATE)(\(\s*)(?P<benchmark3_para1>[A-Za-z0-9_:]*)(,\s*)(?P<benchmark3_para2>[A-Za-z0-9_:]*)(,\s*)(?P<benchmark3_para3>[A-Za-z0-9_:]*)(\))"

CODEBEAMER_LINK = "https://codebeamer.bmwgroup.net/cb/issue/"
REQUIREMENT_TAG_HTTP_NAMED = r"({}(?P<number>\d+))".format(CODEBEAMER_LINK)

regex_trace_unit_tag = re.compile(r"(\@requiredby\s*)(([A-Za-z0-9_]*::[A-Za-z0-9_]+,*\s*)+)", re.MULTILINE)
regex_trace_tag_new_line = re.compile(r"(\s*)(([A-Za-z0-9_]*::[A-Za-z0-9_]+,*\s*)+)", re.MULTILINE)
regex_trace_tag_single_line = r"([@|\\]requirement)\s+((((CB-#)|({}))\d+[,]?[\s]*)+)".format(CODEBEAMER_LINK)
regex_trace_tag_multiline = r"(?:[\/|\*]*)\s+((((CB-#)|({}))\d+[,]?[\s]*)+)?".format(CODEBEAMER_LINK)
regex_trace_comp_tag = re.compile(regex_trace_tag_single_line + regex_trace_tag_multiline, re.MULTILINE)

combined_regex_pattern = re.compile(
    "((?P<test_pattern>%s)|(?P<benchmark1_pattern>%s)|(?P<benchmark2_pattern>%s)|(?P<benchmark3_pattern>%s))"
    % (
        regex_test_pattern,
        BENCHMARK_ONE_PARAMETER_PATTERN,
        BENCHMARK_TWO_PARAMETERS_PATTERN,
        BENCHMARK_THREE_PARAMETERS_PATTERN,
    ),
    re.MULTILINE,
)


def find_test_names(lines):
    traced_tests = []

    matches = [match_object.groupdict() for match_object in combined_regex_pattern.finditer("".join(lines))]
    for match in matches:
        if match["test_pattern"]:
            name = get_test_name(match)
        else:
            name = get_benchmark_name(match)
        traced_tests.append(name)

    return traced_tests


def get_test_name(match):
    return match["suite_name"] + "::" + match["test_name"]


def get_benchmark_name(match):
    if match["benchmark1_pattern"]:
        name = match["benchmark1_para1"] + "::" + "Benchmark"
    elif match["benchmark2_pattern"]:
        name = match["benchmark2_para1"] + "::" + match["benchmark2_para2"]
    elif match["benchmark3_pattern"]:
        name = match["benchmark3_para1"] + "::" + match["benchmark3_para2"] + "_" + match["benchmark3_para3"]
    return name


def split_matches_per_line(relevant_parts_of_match):
    return [match.strip() for match in relevant_parts_of_match.split(",") if match.strip()]


def find_trace_tags_at_index(lines, index, regex_matcher=regex_trace_unit_tag):
    if index < 0 or index >= len(lines):
        return None
    matches = re.findall(regex_matcher, lines[index])
    if matches:
        relevant_parts_of_match = matches[0][1]
        # The regex also matches whitespaces which are filtered out here
        matches_per_line = split_matches_per_line(relevant_parts_of_match)
        handle_special_case_for_multiline_tags(matches_per_line, lines, index)
        for match in matches_per_line:
            named_requirement_number_match = re.match(REQUIREMENT_TAG_HTTP_NAMED, match)
            if named_requirement_number_match:
                requirement_number_dictionary = named_requirement_number_match.groupdict()
                requirement_number = requirement_number_dictionary.get("number")
                requirement_cb = "CB-#" + requirement_number
                matches_per_line.remove(match)
                matches_per_line.append(requirement_cb)
        return list(dict.fromkeys(matches_per_line))
    else:
        # Handle yet another special case where the actual referenced unit test is in a own, new line.
        # Can be caused by clang format
        if lines[index].strip().startswith("/// @requiredby"):
            return handle_special_case_for_referee_per_line(index, lines, matches)
    return None


def handle_special_case_for_referee_per_line(index, lines, matches):
    start_idx = index + 1
    matches = []
    # Loop over every line starting from the requiredby tag and find single line matches for a reference
    while True:
        found_traced_reference = find_trace_tags_at_index(lines, start_idx, regex_matcher=regex_trace_tag_new_line)
        if found_traced_reference:
            matches.extend(found_traced_reference)
            start_idx += 1
        else:
            break
    return matches


def handle_special_case_for_multiline_tags(matches_per_line, lines, index):
    # Special case when the trace tags continue in next line
    new_line_result = find_trace_tags_at_index(lines, index + 1, regex_matcher=regex_trace_tag_new_line)
    if new_line_result:
        matches_per_line.extend(new_line_result)
