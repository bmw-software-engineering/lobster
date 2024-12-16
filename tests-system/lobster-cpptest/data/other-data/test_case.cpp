
/** ensure version are parsed correctly */

/// @version 1
TEST(VersionTagTest, VersionTagTestInOnline) {}

/// @version 1, 42
TEST(VersionTagTest, MultipleVersionTagTestInOnline) {}

/// @requirement CB-#0815
/// @version 12, 70
TEST(VersionTagTest, MoreVersionsThanRequirements) {}

/// @requirement CB-#0815, CB-#0816
/// @version 28
TEST(VersionTagTest, MoreRequirementsThanVersions) {}

/// @requirement CB-#123 CB-#456
/// @version 28 99
TEST(VersionTagTest, VersionSpaceSeparated) {}

/** ensure everything is parsed correctly at once */

///
/// @test foo
/// @brief this test tests something
/// @version 42, 2
/// @requirement CB-#0815, CB-#0816
/// @requiredby FOO0::BAR0
/// @testmethods TM_BOUNDARY, TM_REQUIREMENT
///
TEST(AllTogetherTest, ImplementationMultipleLines) {
	EXPECT_EQ(true, DummyFunctionForValidCondition());
}

/**
 * commented test cases
 */
// TEST(LayoutTest1, SingleComment){}
/* TEST(LayoutTest2, InlineComment){} */
/*
 * TEST(LayoutTest2, Comment) {}
 */

/**
 * invalid test cases
 * 	the following tests should not be parsed
 * 	as valid test cases
 */
TEST(InvalidTest1,) {}
TEST(, InvalidTest2) {}
TEST(,) {}
TEST() {}
