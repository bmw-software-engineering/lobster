load("@lobster_dependencies//:requirements.bzl", "requirement")

py_binary(
    name = "trlc",
    srcs = [
        "conversion_rule.py",
        "conversion_rule_lookup.py",
        "converter.py",
        "errors.py",
        "hierarchy_tree.py",
        "instruction.py",
        "item_wrapper.py",
        "lobster_trlc_config.py",
        "tag_entry.py",
        "text_generation.py",
        "to_string_rules.py",
        "trlc_tool.py",
    ],
    main = "trlc_tool.py",
    data = [
        "schema.yamale",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//:lobster-core",
        "@trlc//trlc",
        requirement("yamale"),
    ],
)
