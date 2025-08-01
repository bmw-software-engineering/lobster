load("//:lobster.bzl", "lobster_raw", "lobster_test", "lobster_trlc")
load("@trlc//:trlc.bzl", "trlc_requirements", "trlc_specification")

trlc_specification(
    name = "req_spec",
    srcs = ["potato.rsl"],
)

trlc_requirements(
    name = "req",
    srcs = ["potato.trlc"],
    spec = [":req_spec"],
)

lobster_trlc(
    name = "software-requirements",
    config = "lobster-trlc.conf",
    requirements = [":req"],
)

lobster_raw(
    name = "system-requirements",
    src = "system-requirements.lobster",
)

lobster_test(
    name = "traceability",
    config = "lobster-bazel.conf",
    inputs = [
        ":software-requirements",
        ":system-requirements",
    ],
)

cc_library(
    name = "foofunc",
    srcs = [
        "foo.cpp",
        "foo.h",
    ],
)

cc_test(
    name = "foo_test",
    srcs = ["test.cpp"],
    deps = [
        "foofunc",
        "//support/gtest/include:lobster_gtest",
        "@googletest//:gtest_main",
    ],
)
