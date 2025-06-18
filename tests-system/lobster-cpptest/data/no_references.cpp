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
why do you want to know the reason just leave me alone
TEST(TestCommentedTest, IAMCommented) {

}
*/
