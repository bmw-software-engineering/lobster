load("@lobster_dependencies//:requirements.bzl", "requirement")

py_binary(
    name = "ci_report-tool",
    srcs = ["ci_report/ci_report.py"],
    main = "ci_report/ci_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster",
    ],
)

py_binary(
    name = "html_report-tool",
    srcs = ["html_report/html_report.py"],
    data = [
        "html_report/assets/html_report.css",
        "html_report/assets/html_report.js",
    ],
    main = "html_report/html_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster",
        requirement("markdown"),
    ],
)

py_binary(
    name = "online_report-tool",
    srcs = ["online_report/online_report.py"],
    main = "online_report/online_report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster",
    ],
)

py_binary(
    name = "report-tool",
    srcs = ["report/report.py"],
    main = "report/report.py",
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster",
    ],
)
