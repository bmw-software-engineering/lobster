import re

from lobster.tools.cpp_parser.parser.tracing.tracing_regex import (
    BENCHMARK_ONE_PARAMETER_PATTERN,
    BENCHMARK_THREE_PARAMETERS_PATTERN,
    BENCHMARK_TWO_PARAMETERS_PATTERN,
)
from lobster.tools.cpp_parser.parser.tracing.tracing_runner import notracing_special_case
from lobster.tools.cpp_parser.parser.config import config
from lobster.tools.cpp_parser.parser.test_case import TestCase

BENCHMARK_CASE_INTRO = re.compile(
    "(BENCHMARK|BENCHMARK_TEMPLATE_F|BENCHMARK_DEFINE_F|BENCHMARK_F|BENCHMARK_CAPTURE|BENCHMARK_TEMPLATE)\("
)


class BenchmarkTestCase(TestCase):
    def __init__(self, file, lines, start_idx):
        TestCase.__init__(self, file, lines, start_idx)

    @staticmethod
    def has_no_macro_or_commented(lines, start_idx):
        return TestCase.has_no_macro_or_commented_general(lines, start_idx, BenchmarkTestCase, BENCHMARK_CASE_INTRO)

    @staticmethod
    def try_parse(file, lines, start_idx):
        """
        Function to parse the given range of lines for a valid benchmark test case.
        If a valid benchmark test case is found a BenchmarkTestCase object is returned, otherwise None
        is returned.

        file -- path to file that the following lines belong to
        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        """
        return TestCase.try_parse_general(file, lines, start_idx, BenchmarkTestCase)

    def _set_test_and_suite_name(self, src):
        match = re.compile(BENCHMARK_THREE_PARAMETERS_PATTERN, re.MULTILINE).search(src)
        if match:
            self.suite_name = match.groupdict().get("benchmark3_para1")
            self.test_name = match.groupdict().get("benchmark3_para2") + "_" + match.groupdict().get("benchmark3_para3")

        match = re.compile(BENCHMARK_TWO_PARAMETERS_PATTERN, re.MULTILINE).search(src)
        if match:
            self.suite_name = match.groupdict().get("benchmark2_para1")
            self.test_name = match.groupdict().get("benchmark2_para2")

        match = re.compile(BENCHMARK_ONE_PARAMETER_PATTERN, re.MULTILINE).search(src)
        if match:
            self.suite_name = match.groupdict().get("benchmark1_para1")
            self.test_name = "Benchmark"

    def _definition_end(self, lines, start_idx):
        """
        This function is searching for the first closing ) bracket after the BENCHMARK macro

        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        """
        line_counter = start_idx
        total_lines = len(lines)
        for index in range(line_counter, total_lines):
            if lines[index].find(")") != -1:
                return index + 1
            else:
                pass
        return start_idx
