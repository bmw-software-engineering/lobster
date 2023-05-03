// 2023 - Florian Schanda
//
// This header file to support LOBSTER tracing in GTests is released
// to the public domain. No other parts of LOBSTER are in the public
// domain, only this specific file.

#ifndef __LOBSTER_GTEST_SUPPORT_H__
#define __LOBSTER_GTEST_SUPPORT_H__

#define LOBSTER_TRACE(prop) \
  ::testing::Test::RecordProperty("lobster-tracing", (prop)),	 \
  ::testing::Test::RecordProperty("lobster-tracing-file", __FILE__),	\
  ::testing::Test::RecordProperty("lobster-tracing-line", __LINE__)

#define LOBSTER_EXCLUDE(reason)					 \
  ::testing::Test::RecordProperty("lobster-exclude", (reason)),	 \
  ::testing::Test::RecordProperty("lobster-tracing-file", __FILE__),	\
  ::testing::Test::RecordProperty("lobster-tracing-line", __LINE__)

#endif
