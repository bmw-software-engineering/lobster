#include <gtest/gtest.h>
#include <lobster_gtest.h>
#include "foo.h"

TEST(ImplicationTest, BasicTest)
{
  LOBSTER_TRACE("example.req_implication");

  EXPECT_TRUE(implication(false, true));
  EXPECT_TRUE(implication(true, true));
}
