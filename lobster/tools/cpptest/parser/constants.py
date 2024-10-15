import re


class Constants:

    NON_EXISTING_INFO = "---"

    CUSTOM_KEY = "custom_key"

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
