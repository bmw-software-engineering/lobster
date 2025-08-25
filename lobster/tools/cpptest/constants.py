import re


class Constants:
    def __init__(self, codebeamer_url = ''):

        self.codebeamer_link = codebeamer_url + "/issue/"
        self.requirement = re.compile(r'@requirement[\s\S]*?(?=@|\Z)')
        self.requirement_tag_http = ((r"([@\\]requirement(\s+"
                                      r"(CB-#\d+\s+)*({}\d+\s*,?\s*/*\*?)+)+)")
                                     .format(self.codebeamer_link))
        self.requirement_tag_http_named = (r"({}(?P<number>\d+))"
                                           .format(self.codebeamer_link))

    NON_EXISTING_INFO = "---"

    LOBSTER_GENERATOR = "lobster-cpptest"

    VALID_TESTMETHODS = [
        "TM_EQUIVALENCE",
        "TM_PAIRWISE",
        "TM_GUESSING",
        "TM_BOUNDARY",
        "TM_CONDITION",
        "TM_REQUIREMENT",
        "TM_TABLE",
    ]

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

    TEST_CASE_INTRO = re.compile(r"^\s*(" +
                                 "|".join(VALID_TEST_MACROS) +
                                 r")\s*\(")
    TEST_CASE_INFO = re.compile(
        r"^\s*(" + "|".join(VALID_TEST_MACROS) +
        r")\s*\(\s*(?P<suite_name>\w+),\s*(?P<test_name>\w+)\)"
    )
    REQUIREMENT_TAG = r"(CB-#\d+)"

    REQUIRED_BY = re.compile(r".*[@\\]requiredby\s+([\s*/]*(\w*::\w+),?\s*)+")
    REQUIRED_BY_TAG = r"(\w*::\w+)"
    DEFECT = re.compile(
        r"(@defect\s+)(((?:(CB-#\d+)|(OCT-#\d+)),?\s*)+)" +
        r"(?:///|/)\s+(((?:(CB-#\d+)|(OCT-#\d+)),?\s)+)?"
    )
    BRIEF = re.compile(r"(@brief\s+)([^@]+)")
    VERSION = re.compile(r"(@version\s+)(\d+([,]? \d+)*)+")
    OCT_TAG = r"(OCT-#\d+)"
    TESTMETHODS = re.compile(r"(@testmethods\s+)([^@]+)")
    TEST = re.compile(r"(@test\s+)([^@]+)")
