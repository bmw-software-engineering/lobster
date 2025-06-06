/** ensure all desired test macros are parsed */

TEST(TestMacrosTest, TestTest) {}

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
    // This comments was added just for testing purposes
    // It doesnt matter what we write here
    // I can write anything I want and nobody cares about it
    EXPECT_EQ(true, DummyFunctionForValidCondition());
    // Writing comments are boring but very important!
}

/* I am a test and commented on purpose because 
why do you want to know the reason just leave me alone.
Just kidding, I am checking if this will be considered by cpptest or not
TEST(TestCommentedTest, IAMCommented) {

}*/
 

// You know what? I am the only test case to have a reference for it.
// @requirement CB-#0815 CB-#0816
TEST(TestWithSingleReference, SingleReference) {}

//
// @requirement https://codebeamer.company.net/cb/issue/0815
//  @requirement CB-#0219
//
TEST(RequirementTagTest2, URLRequirement) {}

//
// @requirement https://codebeamer.company.net/cb/issue/0815,
//              https://codebeamer.company.net/cb/issue/0816
//
TEST(RequirementTagTest2, URLRequirementsCommaSeparated) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, @requirement CB-#0304
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTest2, URLRequirementsAsCommentsSpaceSeparated) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTest2, MultipleURLRequirements) {}

//
// @requirement https://codebeamer.company.net/cb/issue/0815
// @requirement CB-#0816
//
TEST(RequirementTagTest3, MixedRequirements) {}

//
// @requirement something_arbitrary
//
TEST(RequirementTagTest4, InvalidRequirement) {}
