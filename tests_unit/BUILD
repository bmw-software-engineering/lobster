test_suite(
    name = "tests_unit",
    tests = [
        ":test_file_tag_generator",
        ":test_io",
        ":test_io_signal_duplicate_items",
        ":test_items",
        ":test_location",
        ":test_meta_data_tool_base",
        ":test_tool",
    ],
)

py_test(
    name = "test_file_tag_generator",
    srcs = ["test_file_tag_generator.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_io",
    srcs = ["test_io.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_io_signal_duplicate_items",
    srcs = ["test_io_signal_duplicate_items.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_items",
    srcs = ["test_items.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_location",
    srcs = ["test_location.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_meta_data_tool_base",
    srcs = ["test_meta_data_tool_base.py"],
    deps = ["//:lobster-core"],
)

py_test(
    name = "test_tool",
    srcs = ["test_tool.py"],
    deps = ["//:lobster-core"],
)
