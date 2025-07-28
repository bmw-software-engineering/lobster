load("@lobster_dependencies//:requirements.bzl", "requirement")

py_library(
    name = "lobster",
    srcs = glob([
        "lobster/config/*.py",
        "lobster/html/*.py",
        "lobster/*.py",
    ]) + ["//:gen_assets"],
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
    actual = "//lobster/tools/core:ci_report-tool",
)

alias(
    name = "lobster-html-report",
    actual = "//lobster/tools/core:html_report-tool",
)

alias(
    name = "lobster-online-report",
    actual = "//lobster/tools/core:online_report-tool",
)

alias(
    name = "lobster-report",
    actual = "//lobster/tools/core:report-tool",
)
