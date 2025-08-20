load("@lobster_dependencies//:requirements.bzl", "requirement")

py_binary(
    name = "trlc",
    srcs = [
        "conversion_rule_lookup.py",
        "conversion_rule.py",
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
    visibility = ["//visibility:public"],
    data = [
        "schema.yamale",
    ],
    deps = [
        "//:lobster",
        "@trlc//trlc",
        requirement("yamale"),
    ],
)
