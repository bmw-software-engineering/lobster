#include <gtest/gtest.h>
#include "lobster.h"
#include "foo.h"

TEST(ImplicationTest, BasicTest)
{
  LOBSTER_TRACING("example.req_implication");

  EXPECT_TRUE(implication(false, true));
  EXPECT_TRUE(implication(true, true));
}
