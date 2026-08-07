"""Shared package target configuration for package build scripts."""

#Centralized package configuration into a single source of truth

PACKAGE_ORDER = [
    "package_core",
    "package_trlc",
    "package_codebeamer",
    "package_cpp",
    "package_cpp_test",
    "package_gtest",
    "package_json",
    "package_python",
    "package_metapackage",
    "package_monolithic",
]

TOOL_PACKAGE_MAP = {
    "package_trlc": "trlc",
    "package_codebeamer": "codebeamer",
    "package_cpp": "cpp",
    "package_cpp_test": "cpptest",
    "package_gtest": "gtest",
    "package_json": "json",
    "package_python": "python",
}

PACKAGE_DIR_MAP = {
    "package_core": "lobster-core",
    "package_trlc": "lobster-tool-trlc",
    "package_codebeamer": "lobster-tool-codebeamer",
    "package_cpp": "lobster-tool-cpp",
    "package_cpp_test": "lobster-tool-cpptest",
    "package_gtest": "lobster-tool-gtest",
    "package_json": "lobster-tool-json",
    "package_python": "lobster-tool-python",
    "package_metapackage": "lobster-metapackage",
    "package_monolithic": "lobster-monolithic",
}
