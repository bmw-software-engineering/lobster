cc_library(
    name = "fruitfunc",
    srcs = ["fruit.h", "fruit.cpp"]
)

cc_test(
    name = "fruit_test",
    srcs = ["fruit_test.cpp"],
    deps = ["@googletest//:gtest_main",
            "fruitfunc",
	    "//support/gtest/include:lobster_gtest"]
)
