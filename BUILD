load("@lobster_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "lobster-core",
    srcs = glob([
        "lobster/config/*.py",
        "lobster/html/*.py",
        "lobster/tools/core/**/*.py",
        "lobster/*.py",
    ]) + ["//:gen_assets"],
    data = [
        "lobster/tools/core/html_report/assets/html_report.css",
        "lobster/tools/core/html_report/assets/html_report.js",
    ],
    imports = [
        ".",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pyyaml"),
    ],
)

genrule(
    name = "gen_assets",
    srcs = [
        "assets/alert-triangle.svg",
        "assets/award.svg",
        "assets/check-square.svg",
        "assets/chevron-down.svg",
        "assets/external-link.svg",
        "assets/link.svg",
        "assets/menu.svg",
    ],
    outs = ["lobster/html/assets.py"],
    cmd = "$(location //util:mkassets) $(OUTS) $(SRCS)",
    tools = ["//util:mkassets"],
)

alias(
    name = "lobster-json",
    actual = "//lobster/tools/json",
)

alias(
    name = "lobster-trlc",
    actual = "//lobster/tools/trlc",
)

alias(
    name = "lobster-python",
    actual = "//lobster/tools/python",
)

alias(
    name = "lobster-gtest",
    actual = "//lobster/tools/gtest",
)

alias(
    name = "lobster-cpp",
    actual = "//lobster/tools/cpp",
)

alias(
    name = "lobster-ci-report",
    actual = ":ci_report-tool",
)

alias(
    name = "lobster-html-report",
    actual = ":html_report-tool",
)

alias(
    name = "lobster-online-report",
    actual = ":online_report-tool",
)

alias(
    name = "lobster-report",
    actual = ":report-tool",
)

load("@lobster_dependencies//:requirements.bzl", "requirement")

py_binary(
    name = "ci_report-tool",
    srcs = ["lobster/tools/core/ci_report/ci_report.py"],
    main = "lobster/tools/core/ci_report/ci_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster-core",
    ],
)

py_binary(
    name = "html_report-tool",
    srcs = ["lobster/tools/core/html_report/html_report.py"],
    main = "lobster/tools/core/html_report/html_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster-core",
        requirement("markdown"),
    ],
)

py_binary(
    name = "online_report-tool",
    srcs = ["lobster/tools/core/online_report/online_report.py"],
    main = "lobster/tools/core/online_report/online_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster-core",
    ],
)

py_binary(
    name = "report-tool",
    srcs = ["lobster/tools/core/report/report.py"],
    main = "lobster/tools/core/report/report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster-core",
    ],
)
