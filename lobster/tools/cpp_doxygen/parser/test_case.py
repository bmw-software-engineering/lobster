import logging
import re
from typing import Dict, List

from lobster.tools.cpp_doxygen.parser.tracing.tracing_runner import get_range_for_doxygen_comments, notracing_special_case
from lobster.tools.cpp_doxygen.parser.config import config

VALID_TEST_MACROS = [
    "TEST",
    "TEST_P",
    "TEST_F",
    "TYPED_TEST",
    "TYPED_TEST_P",
    "TYPED_TEST_SUITE",
    "TEST_P_INSTANCE",
    "TEST_F_INSTANCE",
]

VALID_TESTMETHODS = [
    "TM_EQUIVALENCE",
    "TM_PAIRWISE",
    "TM_GUESSING",
    "TM_BOUNDARY",
    "TM_CONDITION",
    "TM_REQUIREMENT",
    "TM_TABLE",
    "TM_BOUNDARY",
]

TEST_CASE_INTRO = re.compile(r"^\s*(" + "|".join(VALID_TEST_MACROS) + r")\s*\(")
TEST_CASE_INFO = re.compile(
    r"^\s*(" + "|".join(VALID_TEST_MACROS) + r")\s*\(\s*(?P<suite_name>\w+),\s*(?P<test_name>\w+)\)"
)

CODEBEAMER_LINK = config.codebeamer_url + "/issue/"
REQUIREMENT = re.compile(r".*[@\\]requirement\s+([\s*/]*(((CB-#)|({}))\d+)\s*,?)+".format(CODEBEAMER_LINK))
REQUIREMENT_TAG = r"(CB-#\d+)"
REQUIREMENT_TAG_HTTP = r"([@\\]requirement(\s+(CB-#\d+\s+)*({}\d+\s*,?\s*/*\*?)+)+)".format(CODEBEAMER_LINK)
REQUIREMENT_TAG_HTTP_NAMED = r"({}(?P<number>\d+))".format(CODEBEAMER_LINK)
REQUIRED_BY = re.compile(r".*[@\\]requiredby\s+([\s*/]*(\w*::\w+),?\s*)+")
REQUIRED_BY_TAG = r"(\w*::\w+)"
DEFECT = re.compile(
    r"(@defect\s+)(((?:(CB-#\d+)|(OCT-#\d+)),?\s*)+)" + r"(?:///|/)\s+(((?:(CB-#\d+)|(OCT-#\d+)),?\s)+)?"
)
BRIEF = re.compile(r"(@brief\s+)([^@]+)")
VERSION = re.compile(r"(@version\s+)(\d+([,]? \d+)*)+")
OCT_TAG = r"(OCT-#\d+)"
TESTMETHODS = re.compile(r"(@testmethods\s+)([^@]+)")
# unmatch whole testmethod if invalid method is used
# TESTMETHODS = re.compile(r"(@testmethods\s+)((" + "|".join(VALID_TESTMETHODS) + ")([,]? (" + "|".join(VALID_TESTMETHODS) + "))*)+")
TEST = re.compile(r"(@test\s+)([^@]+)")


class TestCase:
    """
    Class to represent a test case.

    In case of a c/c++ file a test case is considered to be the combination of a
    gtest macro, e.g. TEST(TestSuite, TestName) and its corresponding doxygen style documentation.
    The documentation is assumed to contain references to requirements and related
    test cases.

    Limitations on the tag usage:
    - @requirement, @requiredby & @defect can be used multiple times in the test documentation and can be written on multiple lines
    - @brief, @test, @testmethods and @version can be written on multiple lines but only used once as tag
    """

    def __init__(self, file: str, lines: List[str], start_idx: int):
        self.file_name = file  # File_name where the test case is located
        self.suite_name = config.non_existing_info  # TestSuite from TEST(TestSuite, TestName)
        self.test_name = config.non_existing_info  # TestName from TEST(TestSuite, TestName)
        self.docu_start_line = 1  # First line of the doxygen style doc for the test case
        self.docu_end_line = 1  # Last line of the doxygen style
        self.definition_start_line = (
            1  # First line of the implementation (typically the line TEST(TestSuite, TestName))
        )
        self.definition_end_line = 1  # Last line of the implementation
        self.requirements = []  # List of @requirement values
        self.required_by = []  # List of @requiredby values
        self.defect_tracking_ids = []  # List of @defect values
        self.version_id = []  # Content of @version
        self.test = ""  # Content of @test
        self.testmethods = []  # Content of @testmethods
        self.brief = ""  # Content of @brief

        self._set_test_details(lines, start_idx)

    def _set_test_details(self, lines, start_idx) -> None:
        """
        Parse the given range of lines for a valid test case. Missing information
        are replaced by placeholders.

        file -- path to file that the following lines belong to
        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        """
        self.def_end = self._definition_end(lines, start_idx)

        src = [line.strip() for line in lines[start_idx : self.def_end]]
        src = "".join(src)
        self._set_test_and_suite_name(src)

        self.docu_range = get_range_for_doxygen_comments(lines, start_idx)
        self.docu_start_line = self.docu_range[0] + 1
        self.docu_end_line = self.docu_range[1]
        self.definition_start_line = start_idx + 1
        self.definition_end_line = self.def_end

        if self.docu_range[0] == self.docu_range[1]:
            self.docu_start_line = self.docu_range[0] + 1
            self.docu_end_line = self.docu_start_line

        self.docu_lines = [line.strip() for line in lines[self.docu_range[0] : self.docu_range[1]]]
        self.docu_lines = " ".join(self.docu_lines)
        self._set_base_attributes()

    def _definition_end(self, lines, start_idx, char=["{", "}"]) -> int:
        """
        Function to find the last line of test case defintion, i.e. the closing brace.

        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        """
        nbraces = 0
        while start_idx < len(lines):
            for character in lines[start_idx]:
                if character == char[0]:
                    nbraces = nbraces + 1

                if character == char[1]:
                    nbraces = nbraces - 1
                    if nbraces == 0:
                        return start_idx + 1

            start_idx = start_idx + 1
        return -1

    def _set_test_and_suite_name(self, src) -> None:
        match = TEST_CASE_INFO.search(src)

        if match:
            self.test_name = match.groupdict().get("test_name")
            self.suite_name = match.groupdict().get("suite_name")

    def _set_base_attributes(self) -> None:
        self._get_requirements_from_docu_lines(
            REQUIREMENT, REQUIREMENT_TAG, REQUIREMENT_TAG_HTTP, REQUIREMENT_TAG_HTTP_NAMED
        )

        self.required_by = self._get_require_tags(REQUIRED_BY.search(self.docu_lines), REQUIRED_BY_TAG)

        defect_found = DEFECT.search(self.docu_lines)
        if defect_found:
            defect_tracking_cb_ids = self._get_require_tags(defect_found, REQUIREMENT_TAG)
            cb_list = sorted(
                [
                    '<a href="{1}/issue/{0}">{0}</a>'.format(defect_tracking_id.strip("CB-#"), config.codebeamer_url)
                    for defect_tracking_id in defect_tracking_cb_ids
                ]
            )
            defect_tracking_oct_ids = self._get_require_tags(defect_found, OCT_TAG)
            oct_list = sorted(
                [
                    '<a href="{1}/issue/{0}">{0}</a>'.format(defect_tracking_id.strip("OCT-#"), config.codebeamer_url)
                    for defect_tracking_id in defect_tracking_oct_ids
                ]
            )
            self.defect_tracking_ids = cb_list + oct_list
        self.version_id = self._get_version_tag()
        self.test = self._add_multiline_attribute(TEST)
        self.testmethods = self._get_testmethod_tag()
        self.brief = self._add_multiline_attribute(BRIEF)

    def _get_requirements_from_docu_lines(self, general_pattern, tag, tag_http, tag_http_named):
        """
        Function to search for requirements from docu lines

        general_pattern -- pattern to search for requirements
        tag -- CB-# tag pattern to be searched in docu
        tag_http -- http pattern to be searched in docu
        tag_http_named -- named http pattern to be searched in docu
        """
        search_result = general_pattern.search(self.docu_lines)
        if search_result is None:
            return
        else:
            self.requirements = self._get_require_tags(search_result, tag)
            http_requirements = self._get_require_tags(search_result, tag_http)
            for requirements_listed_behind_one_tag in http_requirements:
                for requirement in requirements_listed_behind_one_tag:
                    requirement_uri = self._get_uri_from_requirement_detection(requirement, tag_http_named)
                    self._add_new_requirement_to_requirement_list(self, requirement_uri, tag_http_named)

    def _get_testmethod_tag(self) -> List[str]:
        """
        Returns a list of string of valid test methods
        If a test method used in the tag is not valid, the value is dropped from the list
        """
        test_methods_list = []
        test_methods = self._add_multiline_attribute(TESTMETHODS)
        for test_method in test_methods.split():
            if test_method in VALID_TESTMETHODS:
                test_methods_list.append(test_method)
            else:
                logging.warning("@testmethod parsing error : " + test_method)
        return test_methods_list

    def _get_version_tag(self) -> List[int]:
        """
        Returns a list of versions as int
        If the number of version specified is less than the number of requirement linked, the last version
        of the list is added for all requirements
        """
        versions = self._add_multiline_attribute(VERSION)
        versions_list = versions.split()
        if versions_list == []:
            versions_list = [float("nan")]
        while len(self.requirements) > len(versions_list):
            last_value = versions_list[-1]
            versions_list.append(last_value)
        return versions_list

    def _add_text_attribute(self, pattern, init_value="") -> str:
        field = init_value
        found = pattern.search(self.docu_lines)
        if found:
            field = found.group(2)
        return field

    def _add_multiline_attribute(self, pattern) -> str:
        field = ""
        found = pattern.search(self.docu_lines)
        if found:
            field = found.group(2).replace("/", " ").replace("*", " ").replace(",", " ") if found else ""
            field = " ".join(field.split())
        return field

    @staticmethod
    def is_line_commented(lines, start_idx) -> bool:
        commented = re.compile(r"^\s*(//|\*|/\*)")
        if commented.match(lines[start_idx]):
            return True
        return False

    @staticmethod
    def has_no_macro_or_commented(lines, start_idx) -> bool:
        return TestCase.has_no_macro_or_commented_general(lines, start_idx, TestCase, TEST_CASE_INTRO)

    @staticmethod
    def has_no_macro_or_commented_general(lines, start_idx, case, case_intro) -> bool:
        """
        Returns True is the test case does not start with an INTRO, or if the test case is commented out
        """
        line = lines[start_idx].strip()

        # If the test case does not start with a :
        # TEST_CASE_INTRO for TestCase
        # BENCHMARK_CASE_INTRO for BenchmarkTestCase
        if not case_intro.match(line):
            return True
        # If the test case is commented out
        elif case.is_line_commented(lines, start_idx):
            return True
        return False

    @staticmethod
    def is_special_case(lines, test_case) -> bool:
        if notracing_special_case(lines, (test_case.docu_start_line - 1, test_case.docu_end_line)):
            return True
        elif test_case.suite_name == config.non_existing_info or test_case.test_name == config.non_existing_info:
            return True

        return False

    @staticmethod
    def try_parse(file, lines, start_idx):
        """
        Function to parse the given range of lines for a valid test case.
        If a valid test case is found a TestCase object is returned, otherwise None
        is returned.

        file -- path to file that the following lines belong to
        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        """
        return TestCase.try_parse_general(file, lines, start_idx, TestCase)

    @staticmethod
    def try_parse_general(file, lines, start_idx, case):
        """
        Function to parse the given range of lines for a valid general case.
        If a valid general case is found a Case object is returned, otherwise None
        is returned.

        file -- path to file that the following lines belong to
        lines -- lines to parse
        start_idx -- index into lines where to start parsing
        case -- test case type
        """
        if case.has_no_macro_or_commented(lines, start_idx):
            # If the test does not follow the convention, None is returned
            return None

        tc = case(file, lines, start_idx)

        if case.is_special_case(lines, tc):
            return None

        return tc

    @staticmethod
    def _get_uri_from_requirement_detection(requirement, tag_http_named):
        """
        Function to get uri itself (without @requirement or similar)

        requirement -- requirement candidate
        tag_http_named -- http pattern to search for uri in requirement candidate
        """
        if requirement == "":
            return None
        else:
            requirement_uri = re.search(tag_http_named, requirement)
            if requirement_uri is None:
                return None
            else:
                return requirement_uri.group()

    @staticmethod
    def _add_new_requirement_to_requirement_list(self, requirement_uri, tag_http_named):
        """
        Function to add new, non-None requirement to requirement list if not included yet

        requirement_uri -- uri to requirement
        tag_http_named -- named http pattern to get requirement number itself
        """
        if requirement_uri is None:
            return
        else:
            named_requirement_number_match = re.match(tag_http_named, requirement_uri)
            requirement_number_dictionary = named_requirement_number_match.groupdict()
            requirement_number = requirement_number_dictionary.get("number")
            requirement_cb = "CB-#" + requirement_number
            if requirement_cb not in self.requirements:
                self.requirements.append(requirement_cb)

    @staticmethod
    def _get_require_tags(match, filter_regex):
        """
        Function to filter the given re.match. The resulting list will only contain
        the objects of the match that correspond to the filter. If the match is
        empty an empty list is returned.

        match -- re.match object
        filter_regex -- filter to apply to the match
        """

        if not match:
            return []

        return re.findall(filter_regex, match.group(0))

    @staticmethod
    def _search_start_line(lines, start_idx):
        comments = ["///", "//", "/*", "*"]
        index_pointer = start_idx
        while index_pointer < len(lines):
            if any(x in lines[index_pointer] for x in comments):
                index_pointer += 1
            else:
                break
        start_idx = index_pointer
        return start_idx

    @staticmethod
    def _read_file(file):
        try:
            with open(file, "r", encoding="UTF-8", errors="ignore") as f:
                lines = f.readlines()

        except Exception as e:
            logging.error(f"exception {e}")
            lines = []
        return lines
