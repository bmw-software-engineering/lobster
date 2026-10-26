# LOBSTER - Lightweight Open BMW Software Traceability Evidence Report
# Copyright (C) 2026 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
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

import unittest

from lobster.tools.gtest.givenwhenthen import GivenWhenThen


class GivenWhenThenTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    CAMEL_CASE_CASES = (
        ("KernelLargerThanSignal", "kernel larger than signal"),
        ("Prototype", "prototype"),
        ("A", "a"),
        ("ABC", "abc"),
        ("HTTPServer", "http server"),
        ("ServerHTTP", "server http"),
        ("ValidPMRAllocator", "valid pmr allocator"),
        ("Port80Open", "port 80 open"),
        ("StackWith3Elements", "stack with 3 elements"),
        ("Base64Encoded", "base 64 encoded"),
        ("3Items", "3 items"),
        ("Urls", "urls"),
        ("IPv4", "i pv 4"),
    )

    NON_MATCHING_NAMES = (
        "",
        "/",
        "PlainName",
        "givenA_ExpectB",
        "Givena_ExpectB",
        "GivenA",
        "GivenA_WhenB",
        "Given_A_ExpectB",
        "GivenA_Expect_B",
        "GivenA_Expect",
        "GivenA_ExpectedFailure",
        "GivenA_Thenb",
        "GivenA_WhenB_ThenC_",
        "GivenA_WhenB_ThenC_Extra",
        "GivenA_AndB_ExpectC",
        "GivenA_WhenB_AndC_ExpectD",
        "GivenA_WhenB_WhenC_ExpectD",
        "GivenSize_0_ExpectEmpty",
        "Too_Many_GivenA_ExpectB",
        "Prefix_GivenA_ExpectB_Suffix",
        "PrefixGivenA_ExpectB",
        "Whenever_GivenA_ExpectB_",
        "GivenA_WhenB_ExpectC_ThenD",
        "GivenA-B_ExpectC",
        "GivenA B_ExpectC",
        "Given\u00c4_ExpectB",
        "GivenA_ExpectB\n",
    )

    def test_extracts_all_parts(self):
        """Test that all three parts are extracted from a full name."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name with a Given, When and Expect part
        name = "GivenEmptyStack_WhenPopCalled_ExpectError"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN all parts are set
        self.assertEqual(
            GivenWhenThen(given="empty stack", when="pop called", then="error"),
            spec,
        )

    def test_accepts_then_instead_of_expect(self):
        """Test that a Then part is accepted instead of an Expect part."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name which uses "Then"
        name = "GivenA_WhenB_ThenC"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the Then part is set
        self.assertEqual(GivenWhenThen(given="a", when="b", then="c"), spec)

    def test_when_part_is_optional(self):
        """Test that a name without When part gives an empty when."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name without When part
        name = "GivenEmptyStack_ExpectSizeZero"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the when part is empty
        self.assertEqual(
            GivenWhenThen(given="empty stack", when="", then="size zero"), spec
        )

    def test_accepts_prefix(self):
        """Test that a leading alphanumeric prefix is ignored."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name with a prefix
        name = "Push_GivenFull_WhenPush_ExpectOverflow"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the prefix does not appear in any part
        self.assertEqual(
            GivenWhenThen(given="full", when="push", then="overflow"), spec
        )

    def test_accepts_prefix_with_digits(self):
        """Test that a prefix may contain digits."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name with a prefix containing a digit
        name = "Case2_GivenA_ExpectB"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the parts are set
        self.assertEqual(GivenWhenThen(given="a", when="", then="b"), spec)

    def test_accepts_parts_starting_with_a_digit(self):
        """Test that parts may start with a digit."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name whose parts start with digits
        name = "Given3Items_When2Calls_Then1Result"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the parts are set
        self.assertEqual(
            GivenWhenThen(given="3 items", when="2 calls", then="1 result"),
            spec,
        )

    def test_accepts_parameter_index_segment(self):
        """Test that a trailing parameter index segment is ignored."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name with a parameter index
        name = "GivenA_ExpectB/0"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the parts are set
        self.assertEqual(GivenWhenThen(given="a", when="", then="b"), spec)

    def test_part_may_contain_given_when_and_then_words(self):
        """Test that keywords inside a part are not mistaken for keywords."""
        # lobster-trace: gtest_req.From_Test_Name_Extracts_Parts
        # GIVEN a test name whose parts start with the words of the keywords
        name = "GivenWhenX_WhenThenY_ThenGivenZ"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the words are part of the values
        self.assertEqual(
            GivenWhenThen(given="when x", when="then y", then="given z"), spec
        )

    def test_converts_camel_case_to_lower_case_words(self):
        """Test the conversion of CamelCase text to lower case words."""
        # lobster-trace: gtest_req.From_Test_Name_Converts_CamelCase_To_Words
        for camel_case, words in self.CAMEL_CASE_CASES:
            with self.subTest(camel_case=camel_case):
                # GIVEN a test name with the CamelCase text as Given part
                name = f"Given{camel_case}_ExpectX"

                # WHEN the specification is derived from the name
                spec = GivenWhenThen.from_test_name(name)

                # THEN the Given part consists of lower case words
                self.assertEqual(words, spec.given)

    def test_last_matching_segment_wins(self):
        """Test that the last of several matching segments is used."""
        # lobster-trace: gtest_req.From_Test_Name_Uses_Last_Matching_Segment
        # GIVEN a test name with several matching segments
        name = "Inst/GivenA_ExpectA/GivenB_ExpectB/3"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the parts of the last matching segment are used
        self.assertEqual(GivenWhenThen(given="b", when="", then="b"), spec)

    def test_non_matching_segments_are_skipped(self):
        """Test that non-matching segments do not replace a match."""
        # lobster-trace: gtest_req.From_Test_Name_Uses_Last_Matching_Segment
        # GIVEN a matching segment followed by a non-matching one
        name = "Inst/GivenA_ExpectA/ExpectedFailure"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN the parts of the matching segment are used
        self.assertEqual(GivenWhenThen(given="a", when="", then="a"), spec)

    def test_segment_with_when_replaces_segment_without(self):
        """Test that a later segment replaces all parts of an earlier one."""
        # lobster-trace: gtest_req.From_Test_Name_Uses_Last_Matching_Segment
        # GIVEN an earlier segment without When and a later one with When
        name = "GivenA_ExpectB/GivenC_WhenD_ExpectE"

        # WHEN the specification is derived from the name
        spec = GivenWhenThen.from_test_name(name)

        # THEN all parts come from the later segment
        self.assertEqual(GivenWhenThen(given="c", when="d", then="e"), spec)

    def test_names_which_do_not_match_completely_give_empty_specification(self):
        """Test that a name without a complete match gives no parts."""
        # lobster-trace: gtest_req.From_Test_Name_Requires_Complete_Match
        for name in self.NON_MATCHING_NAMES:
            with self.subTest(name=name):
                # GIVEN a test name which does not match completely
                # WHEN the specification is derived from the name
                spec = GivenWhenThen.from_test_name(name)

                # THEN no part is set
                self.assertEqual(GivenWhenThen(), spec)

    def test_merge_appends_parts_in_given_when_then_order(self):
        """Test that parts are appended in the order Given, When, Then."""
        # lobster-trace: gtest_req.Merge_Appends_Parts_In_Order
        # GIVEN a specification and one unrelated property
        spec = GivenWhenThen(then="c", when="b", given="a")
        properties = [("Description", "d")]

        # WHEN the specification is merged into the properties
        merged = spec.merge_into(properties)

        # THEN the parts follow the property in the order Given, When, Then
        self.assertEqual(
            [("Description", "d"), ("Given", "a"), ("When", "b"), ("Then", "c")],
            merged,
        )

    def test_merge_does_not_change_the_given_list(self):
        """Test that merging leaves the passed list untouched."""
        # lobster-trace: gtest_req.Merge_Appends_Parts_In_Order
        # GIVEN a specification and a list of properties
        spec = GivenWhenThen(given="a")
        properties = [("Description", "d")]

        # WHEN the specification is merged into the properties
        spec.merge_into(properties)

        # THEN the list still has its original content
        self.assertEqual([("Description", "d")], properties)

    def test_merge_skips_empty_parts(self):
        """Test that empty parts are not appended."""
        # lobster-trace: gtest_req.Merge_Appends_Parts_In_Order
        # GIVEN a specification without When part
        spec = GivenWhenThen(given="a", then="c")

        # WHEN the specification is merged into no properties
        merged = spec.merge_into([])

        # THEN only Given and Then are present
        self.assertEqual([("Given", "a"), ("Then", "c")], merged)

    def test_merge_replaces_properties_of_the_same_name(self):
        """Test that blank properties are replaced by the parts."""
        # lobster-trace: gtest_req.Merge_Replaces_Blank_Properties
        # GIVEN a specification and blank Given and Then properties
        spec = GivenWhenThen(given="a", then="c")
        properties = [("Given", ""), ("Description", "d"), ("Then", "  ")]

        # WHEN the specification is merged into the properties
        merged = spec.merge_into(properties)

        # THEN the blank properties are replaced and the others are kept
        self.assertEqual(
            [("Description", "d"), ("Given", "a"), ("Then", "c")], merged
        )

    def test_merge_keeps_properties_for_which_there_is_no_part(self):
        """Test that a property is kept if the specification lacks its part."""
        # lobster-trace: gtest_req.Merge_Replaces_Blank_Properties
        # GIVEN a specification without When and a blank When property
        spec = GivenWhenThen(given="a", then="c")

        # WHEN the specification is merged into the properties
        merged = spec.merge_into([("When", "")])

        # THEN the When property is kept
        self.assertEqual([("When", ""), ("Given", "a"), ("Then", "c")], merged)

    def test_merge_of_empty_specification_leaves_properties_unchanged(self):
        """Test that an empty specification does not change properties."""
        # lobster-trace: gtest_req.Merge_Leaves_Properties_Unchanged_Without_Parts
        # GIVEN an empty specification and properties incl. blank ones
        properties = [("Given", ""), ("Description", "d"), ("Then", "t")]

        # WHEN the specification is merged into the properties
        merged = GivenWhenThen().merge_into(properties)

        # THEN the properties are unchanged
        self.assertEqual(properties, merged)

    def test_non_blank_part_property_conflicts(self):
        """Test that a non-blank Given, When or Then property conflicts."""
        # lobster-trace: gtest_req.Conflicts_With_Detects_Non_Blank_Spec_Properties
        # GIVEN a specification with parts
        spec = GivenWhenThen(given="a", then="c")
        for name in ("Given", "When", "Then"):
            with self.subTest(name=name):
                # WHEN it is checked against a non-blank property
                result = spec.conflicts_with([(name, "x")])

                # THEN there is a conflict, even if the spec lacks that part
                self.assertTrue(result)

    def test_blank_properties_do_not_conflict(self):
        """Test that empty and whitespace-only properties do not conflict."""
        # lobster-trace: gtest_req.Conflicts_With_Detects_Non_Blank_Spec_Properties
        # GIVEN a specification with parts
        spec = GivenWhenThen(given="a", then="c")

        # WHEN it is checked against blank properties
        result = spec.conflicts_with([("Given", ""), ("Then", " \t")])

        # THEN there is no conflict
        self.assertFalse(result)

    def test_other_properties_do_not_conflict(self):
        """Test that properties with other names do not conflict."""
        # lobster-trace: gtest_req.Conflicts_With_Detects_Non_Blank_Spec_Properties
        # GIVEN a specification with parts
        spec = GivenWhenThen(given="a", then="c")

        # WHEN it is checked against a non-blank Description property
        result = spec.conflicts_with([("Description", "x")])

        # THEN there is no conflict
        self.assertFalse(result)

    def test_empty_specification_never_conflicts(self):
        """Test that an empty specification does not conflict."""
        # lobster-trace: gtest_req.Conflicts_With_Detects_Non_Blank_Spec_Properties
        # GIVEN an empty specification
        spec = GivenWhenThen()

        # WHEN it is checked against a non-blank Given property
        result = spec.conflicts_with([("Given", "x")])

        # THEN there is no conflict
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
