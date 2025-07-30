/** ensure all desired test macros are parsed */

TEST_P_INSTANCE(TestMacrosTest, TestPInstance) {}
TEST(TestMacrosTest, TestTest) {}
TEST_F(TestMacrosTest1, TestTestF) {}
TEST_P(TestMacrosTest1, TestTestP) {}
TYPED_TEST(TestMacrosTest2, TestTypedTest) {}
TYPED_TEST_P(TestMacrosTest2, TestTypedTestP) {}
TYPED_TEST_SUITE(TestMacrosTest2, TestTypedTestSuite) {}
TEST_F_INSTANCE(TestMacrosTest3, TestFInstance) {}

/** ensure test implementation is correctly parsed */

TEST(
    ImplementationTest,
    TestMultiLine
) {}

TEST(ImplementationTest, EmptyImplementation) {}

TEST(ImplementationTest, ImplementationMultipleLines) {
    EXPECT_EQ(true, DummyFunctionForValidCondition());
}

TEST(ImplementationTest, MultipleLinesWithComments)
{
    // Some comments
    EXPECT_EQ(true, DummyFunctionForValidCondition());
    // Some other comments
}

/** ensure test tag is correctly parsed */

/// @test foo1
TEST(TestTagTest, TestTagInOnline) {}

///
/// @test foo2
TEST(TestTagTest, TestTagPrecededByComment) {}

/// @test foo3
///
TEST(TestTagTest, TestTagFollowedByComment) {}

///
/// @test foo4
///
TEST(TestTagTest, TestTagWithCommentsAround) {}

/// @test lorem ipsum
TEST(TestTagTest, TestTagAsText) {}

/** ensure brief are parsed correctly */

/// @brief Some nasty bug1
TEST(BriefTagTest, BriefTagInOnline) {}

/// @brief This is a brief field
/// with a long description
TEST(BriefTagTest, BriefTagMultipleLines) {}

/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTest, Requirement) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTest1, RequirementAsOneLineComments) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTest1, RequirementAsComments) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTest1, RequirementsAsMultipleComments) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTest2, URLRequirement) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTest2, URLRequirementsCommaSeparated) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTest2, URLRequirementsAsCommentsSpaceSeparated) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTest2, MultipleURLRequirements) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTest3, MixedRequirements) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTest4, InvalidRequirement) {}

///
/// @requirement 
///
TEST(RequirementTagTest4, MissingRequirementReference) {}

/** ensure required-by tags are parsed correctly */

///
/// @requiredby FOO0::BAR0
///
TEST(RequirementByTest1, RequiredByWithAt) {}

///
/// @requiredby FOO0::BAR0, FOO1::BAR1
///
TEST(RequirementByTest1, MultipleRequiredByCommaSeparated) {}

/**
 * @requiredby FOO0::BAR0, FOO1::BAR1,
 * 			   FOO2::BAR2
 * @requiredby FOO3::BAR3 FOO4::BAR4,
 * 			   FOO5::BAR5
 * @requiredby FOO6::BAR6 FOO7::BAR7
 * 			   FOO8::BAR8
 */
TEST(RequirementByTest1, MultipleRequiredByAsComments) {}

/// @test lorem ipsum
/// @requiredby FOO0::BAR0,
///             FOO1::BAR1,
/// 			FOO2::BAR2,
///             FOO3::BAR3,
///             FOO4::BAR4,
/// 			FOO5::BAR5,
///             FOO6::BAR6,
///             FOO7::BAR7,
/// 			FOO8::BAR8
///
TEST(RequirementByTest2, RequiredByWithNewLines) {}

/** ensure testmethods are parsed correctly */

/// @testmethods TM_REQUIREMENT
TEST(TestMethodsTagTest, TestMethod) {}

/**
 * @testmethods TM_PAIRWISE TM_BOUNDARY
 */
TEST(TestMethodsTagTest2, TestMethodAsCommentsSpaceSeparated) {}

/// @testmethods TM_REQUIREMENT, TM_EQUIVALENCE
TEST(TestMethodsTagTest2,  TestMethodAsCommentsCommaSeparated) {}

// /// @testmethods TM_REQUIREMENT, TM_EQUIVALENCE
// /// @testmethods TM_BOUNDARY, TM_CONDITION
// TEST(TestMethodsTagTest2,  TestMethodAsCommentsMultipleLines) {}

///
/// @testmethods something_arbitrary
///
TEST(TestMethodsTagTest3, InvalidTestMethod) {}

///
/// @testmethods 
///
TEST(TestMethodsTagTest4, MissingTestMethod) {}

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
/* 
@requirement
@requirement CB-#0815, CB-#0816
@requirement https://codebeamer.company.net/cb/issue/0815
TEST(LayoutTest1, SingleComment){}
*/

/* TEST(LayoutTest2, InlineComment){} */
/*
 * TEST(LayoutTest3, Comment) {}
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
