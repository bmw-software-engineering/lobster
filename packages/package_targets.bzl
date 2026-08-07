"""Macros for generating package builder targets."""

load("@rules_python//python:defs.bzl", "py_binary")
load("//:requirements.bzl", "requirement")

def lobster_package_target(name):
    """Create a py_binary wrapper for a single package_builder target."""
    py_binary(
        name = name,
        main = "package_builder.py",
        srcs = [
            "package_builder.py",
            "package_config.py",
        ],
        args = [name],
        visibility = ["//visibility:public"],
        deps = [
            requirement("build"),
        ],
    )

def lobster_package_targets(names):
    """Create py_binary wrappers for all package_builder targets."""
    for name in names:
        lobster_package_target(name)
