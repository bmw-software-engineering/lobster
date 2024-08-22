import re

# URLs
GIT_BASEDIR = "/vispiron-swe"
GITHUB_URL = "https://github.com/"
CODEBEMAER_URL = "https://codebeamer.bmwgroup.net/cb"


NON_EXISTING_INFO = "---"

LOBSTER_GENERATOR = "lobster_cpp_doxygen"

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


# Regex
TEST_CASE_INTRO = re.compile(r"^\s*(" + "|".join(VALID_TEST_MACROS) + r")\s*\(")
TEST_CASE_INFO = re.compile(
    r"^\s*(" + "|".join(VALID_TEST_MACROS) + r")\s*\(\s*(?P<suite_name>\w+),\s*(?P<test_name>\w+)\)"
)

CODEBEAMER_LINK = CODEBEMAER_URL + "/issue/"
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