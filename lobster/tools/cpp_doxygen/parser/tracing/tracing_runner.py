# Copyright (C) 2020, Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
# pylint: disable=logging-format-interpolation

import re
import sys
import argparse
import logging
from termcolor import colored
from pprint import pformat

from lobster.tools.cpp_doxygen.parser.tracing.tracing_helpers import (
    read_list_of_test_files_from_tracing_aspect_file_names,
    get_absolute_file_path,
)
from lobster.tools.cpp_doxygen.parser.tracing.tracing_results import TracingUnitResult, TracingComponentResult
from lobster.tools.cpp_doxygen.parser.tracing.tracing_regex import (
    find_test_names,
    find_trace_tags_at_index,
    regex_trace_unit_tag,
    regex_trace_comp_tag,
)


def loop_tests(all_tests, unit_test_name, test_references):
    correct_reference = []
    incorrect_reference = []

    for test_reference in test_references:
        logging.debug(f"Looking for test reference {test_reference}")
        if test_reference in all_tests:
            logging.debug(f"Correct reference from unit test '{unit_test_name}' to test '{test_reference}'")
            correct_reference.append(unit_test_name)
        else:
            logging.warning(
                colored(f"Test '{test_reference}' referenced from '{unit_test_name}' does not exist", "yellow")
            )
            incorrect_reference.append(unit_test_name)
    return correct_reference, incorrect_reference


def match_tracing(all_tests, all_unit_tests_with_references):
    correct_reference = []
    missing_reference = []
    incorrect_reference = []

    for unit_test_name, test_references in all_unit_tests_with_references.items():
        if not test_references:
            missing_reference.append(unit_test_name)
            continue
        correct, incorrect = loop_tests(all_tests, unit_test_name, test_references)
        correct_reference.extend(correct)
        incorrect_reference.extend(incorrect)

    return correct_reference, missing_reference, incorrect_reference


def match_unit_tests_with_other_tests(component_test_files, unit_tests_files):
    all_tests = []
    all_unit_tests_with_references = {}

    for component_test_file in component_test_files:
        component_tests = find_test_names_for_file(component_test_file)
        all_tests.extend(component_tests)

        logging.debug(f"Found {len(component_tests)} component tests in {component_test_file}")

    for unit_test_file in unit_tests_files:
        unit_tests = find_test_names_for_file(unit_test_file)
        all_tests.extend(unit_tests)

        logging.debug(f"Found {len(unit_tests)} unit tests in {unit_test_file}")

        unit_tests_with_reference = map_test_names_with_trace_tags(unit_test_file)
        all_unit_tests_with_references.update(unit_tests_with_reference)

        logging.debug(f"File {unit_test_file} contains unit tests with references {unit_tests_with_reference}")

    return match_tracing(all_tests, all_unit_tests_with_references)


def apply_rule_on_lines(lines, regex_trace_tags):
    test_macro_regex = r"^(TEST|(BENCHMARK|BENCHMARK_DEFINE_F|BENCHMARK_F|BENCHMARK_TEMPLATE_F|BENCHMARK_CAPTURE|BENCHMARK_TEMPLATE)(\()|(TYPED_TEST(?!(_CASE|_SUITE)))).*"
    skip_test_macro_regex = r"^(TEST_F_CALL|TEST_P_CALL)(\().*"
    unit_tests_to_trace_tags = {}
    for index, _ in enumerate(lines):
        # To overcome the multiline regex parsing (we are searching in a range lines[index:], which
        # would result in false positives when we start searching before the actual TEST macro)
        if not re.match(test_macro_regex, lines[index]) or re.match(skip_test_macro_regex, lines[index]):
            continue
        matched_test_name = find_first_test_name(lines[index:])
        if matched_test_name:
            logging.debug(f"Found unit test name {matched_test_name}")
            the_range = get_range_for_doxygen_comments(lines, index)

            if not notracing_special_case(lines, the_range):
                matched_trace_tags = find_trace_tag_in_range(lines, range(the_range[0], the_range[1]), regex_trace_tags)
                if matched_trace_tags:
                    logging.debug(f"Found trace to other test(s) {matched_trace_tags}")
                    unit_tests_to_trace_tags[matched_test_name] = matched_trace_tags
                else:
                    unit_tests_to_trace_tags[matched_test_name] = None
    return unit_tests_to_trace_tags


def map_test_names_with_trace_tags(file_name, regex_trace_tags=regex_trace_unit_tag):
    with open(get_absolute_file_path(file_name)) as the_file:
        lines = the_file.readlines()
        unit_tests_to_trace_tags = apply_rule_on_lines(lines, regex_trace_tags)

    return unit_tests_to_trace_tags


def notracing_special_case(lines, the_range):
    notracing_tag = "NOTRACING"
    return list(filter(lambda x: notracing_tag in x, lines[the_range[0] : the_range[1]]))


def get_range_for_doxygen_comments(lines, index_of_test_definition):
    comments = ["///", "//", "/*", "*"]
    has_at_least_one_comment = True
    index_pointer = index_of_test_definition - 1
    while index_pointer > 0:
        if any(x in lines[index_pointer] for x in comments):
            index_pointer -= 1
        else:
            has_at_least_one_comment = False
            break
    start_index = index_pointer if has_at_least_one_comment else index_pointer + 1
    doxygen_comments_line_range = (start_index, index_of_test_definition)
    return doxygen_comments_line_range


def find_trace_tag_in_range(lines, search_range, regex_trace_tags=regex_trace_unit_tag):
    trace_tags = []
    for index in search_range:
        trace_tags_per_line = find_trace_tags_at_index(lines, index, regex_trace_tags)
        if trace_tags_per_line:
            trace_tags.extend(trace_tags_per_line)
    return list(dict.fromkeys(trace_tags))


def find_first_test_name(lines):
    test_names = find_test_names(lines)
    if test_names:
        return test_names[0]
    return None


def find_test_names_for_file(test_file_name):
    test_file_name_pah = get_absolute_file_path(test_file_name)
    test_file_content = []
    with open(test_file_name_pah) as f:
        test_file_content = "".join(f.readlines())
    return find_test_names(test_file_content)


def present_unit_summary(correct_reference, missing_reference, incorrect_reference, log_function):
    log_function(colored("Summary:", attrs=["bold"]))
    log_function(colored(f"Number of correct references: {len(correct_reference)}", "green"))
    log_function(colored(f"Number of missing references: {len(missing_reference)}", "red"))
    log_function(colored(f"Number of incorrect references: {len(incorrect_reference)}", "red"))

    set_of_missing_reference = sorted(set(missing_reference))
    if set_of_missing_reference:
        log_function(
            colored(f"Missing reference(s) for these test(s):\n{pformat(set_of_missing_reference)}", attrs=["dark"])
        )

    set_of_incorrect_reference = sorted(set(incorrect_reference))
    if set_of_incorrect_reference:
        log_function(
            colored(f"Incorrect reference(s) for these test(s):\n{pformat(set_of_incorrect_reference)}", attrs=["dark"])
        )


def present_component_summary(available_requirement_tags, missing_requirement_tags, log_function):
    log_function(colored("Summary:", attrs=["bold"]))
    log_function(colored(f"Number of available requirement tags: {len(available_requirement_tags)}", "green"))
    log_function(colored(f"Number of missing requirement tags: {len(missing_requirement_tags)}", "red"))

    set_of_missing_requirement_tags = set(sorted(missing_requirement_tags))
    if set_of_missing_requirement_tags:
        log_function(
            colored(
                f"Missing requirement tag(s) for these test(s):\n{pformat(set_of_missing_requirement_tags)}",
                attrs=["dark"],
            )
        )


def get_component_test_names_with_trace_tags(component_test_files):
    all_component_tests_with_references = {}
    for component_test_file in component_test_files:
        all_component_tests_with_references.update(
            map_test_names_with_trace_tags(component_test_file, regex_trace_comp_tag)
        )
    return all_component_tests_with_references


def get_component_tests_tracing_result(component_test_files):
    available_requirement_tags = []
    missing_requirement_tags = []
    all_component_tests_with_references = get_component_test_names_with_trace_tags(component_test_files)
    for component_test, reference in all_component_tests_with_references.items():
        if reference:
            available_requirement_tags.append(component_test)
        else:
            missing_requirement_tags.append(component_test)

    return available_requirement_tags, missing_requirement_tags


def create_referenced_unit_tracing_rule(all_component_test_files, all_unit_tests_files):
    correct_reference, missing_reference, incorrect_reference = match_unit_tests_with_other_tests(
        all_component_test_files, all_unit_tests_files
    )
    tracing_results = TracingUnitResult(
        correct_references=correct_reference,
        missing_references=missing_reference,
        incorrect_references=incorrect_reference,
    )
    return tracing_results


def create_referenced_component_tracing_rule(all_component_test_files, ignore_missing):
    available_requirement_tags, missing_requirement_tags = get_component_tests_tracing_result(all_component_test_files)
    tracing_results = TracingComponentResult(
        available_requirement_tags=available_requirement_tags, missing_requirement_tags=missing_requirement_tags
    )
    return tracing_results


def merge_unit_and_component_results(tracing_results_unit, tracing_results_component, ignore_missing_requirements):
    available_component = set(tracing_results_component.available)
    missing_component = set(tracing_results_component.missing)

    correct_unit = set(tracing_results_unit.correct)
    missing_unit = set(tracing_results_unit.missing)
    incorrect_unit = set(tracing_results_unit.incorrect)

    # Ignore missing unit linkages if flagged
    if ignore_missing_requirements:
        missing_unit = set()
        missing_component = set()

    is_subset_component = missing_component.issubset(correct_unit)
    is_subset_unit = missing_unit.issubset(available_component)

    violation_set_component = missing_component - correct_unit
    violation_set_unit = missing_unit - available_component
    all_unit_violations = violation_set_unit | incorrect_unit

    if all_unit_violations:
        present_unit_summary(correct_unit, violation_set_unit, incorrect_unit, logging.warning)
    if violation_set_component:
        present_component_summary(available_component, violation_set_component, logging.warning)

    success = is_subset_component and is_subset_unit and not incorrect_unit
    return success, violation_set_component, all_unit_violations


def run_trace(output_file_path, component_test, unit_test, ignore_missing):
    all_component_test_files = read_list_of_test_files_from_tracing_aspect_file_names(component_test)
    all_unit_tests_files = read_list_of_test_files_from_tracing_aspect_file_names(unit_test)

    all_test_files = all_component_test_files + all_unit_tests_files

    tracing_results_unit = create_referenced_unit_tracing_rule(all_test_files, all_test_files)
    tracing_results_component = create_referenced_component_tracing_rule(all_test_files, ignore_missing)

    present_unit_summary(
        tracing_results_unit.correct, tracing_results_unit.missing, tracing_results_unit.incorrect, logging.info
    )
    present_component_summary(tracing_results_component.available, tracing_results_component.missing, logging.info)

    with open(output_file_path, "w") as file:
        file.write(
            (
                f"Tracing Results (Component)\n{str(tracing_results_component)}\n"
                f"Tracing Results (Unit)\n{str(tracing_results_unit)}"
            )
        )

    return tracing_results_component, tracing_results_unit


def main():
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s", datefmt="%H:%M:%S")

    args = parse_arguments()

    output_file_name = args.output[0]
    tracing_results_component, tracing_results_unit = run_trace(
        output_file_name, args.test_targets, args.unit_tests, args.ignore_missing_requirements
    )

    ignore_errors = args.ignore_errors
    ignore_missing_requirements = args.ignore_missing_requirements

    success, violation_set_component, violation_set_unit = merge_unit_and_component_results(
        tracing_results_unit, tracing_results_component, ignore_missing_requirements
    )
    merged_violations = violation_set_component | violation_set_unit

    if success or ignore_errors:
        sys.exit(0)
    else:
        logging.error(colored("Result:", attrs=["bold"]))
        logging.error(colored(f"Found {len(merged_violations)} failure(s), please check the test(s)", "red"))
        sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser()
    required_named = parser.add_argument_group("required named arguments")
    required_named.add_argument(
        "--output", nargs="+", help="The output file path results are written to", required=True
    )
    required_named.add_argument(
        "--test_targets", nargs="+", help="A file containing a list of component test files", required=True
    )
    parser.add_argument("--unit_tests", nargs="+", help="A file containing a list of unit test files", default=[])
    parser.add_argument("--ignore_errors", action="store_true", help="Ignores errors")
    parser.add_argument("--ignore_missing_requirements", action="store_true", help="Ignores missing requirements")
    args = parser.parse_args()
    return args


if __name__ == "__main__":  # pragma: no cover
    main()
