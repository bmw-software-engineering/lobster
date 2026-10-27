#include <gtest/gtest.h>

TEST(Stack, GivenEmptyStack_ExpectSizeZero) {
  ::testing::Test::RecordProperty("lobster-tracing", "stack.size");
  EXPECT_EQ(0, 0);
}
