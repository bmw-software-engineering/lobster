#ifndef __LOBSTER_TRACING_H__
#define __LOBSTER_TRACING_H__

#define LOBSTER_TRACING(prop) \
  ::testing::Test::RecordProperty("lobster-tracing", (prop)),	 \
  ::testing::Test::RecordProperty("lobster-tracing-file", __FILE__),	\
  ::testing::Test::RecordProperty("lobster-tracing-line", __LINE__)

#endif
