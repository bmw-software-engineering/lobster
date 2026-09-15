"""Bazel packaging targets for setuptools-backed LOBSTER wheels."""

PACKAGE_SPECS = {
    "lobster-core": {"kind": "core"},
    "lobster-tool-trlc": {"kind": "tool", "tool": "trlc"},
    "lobster-tool-codebeamer": {"kind": "tool", "tool": "codebeamer"},
    "lobster-tool-cpp": {"kind": "tool", "tool": "cpp"},
    "lobster-tool-cpptest": {"kind": "tool", "tool": "cpptest"},
    "lobster-tool-gtest": {"kind": "tool", "tool": "gtest"},
    "lobster-tool-json": {"kind": "tool", "tool": "json"},
    "lobster-tool-python": {"kind": "tool", "tool": "python"},
    "lobster-metapackage": {"kind": "meta"},
    "lobster-monolithic": {"kind": "mono"},
}

PACKAGE_ORDER = [
    "lobster-core",
    "lobster-tool-trlc",
    "lobster-tool-codebeamer",
    "lobster-tool-cpp",
    "lobster-tool-cpptest",
    "lobster-tool-gtest",
    "lobster-tool-json",
    "lobster-tool-python",
    "lobster-metapackage",
    "lobster-monolithic",
]

SMOKE_TEST_COMMANDS = [
    "lobster-report",
    "lobster-ci-report",
    "lobster-html-report",
    "lobster-online-report",
    "lobster-online-report-nogit",
    "lobster-cpp",
    "lobster-cpptest",
    "lobster-codebeamer",
    "lobster-gtest",
    "lobster-json",
    "lobster-python",
    "lobster-trlc",
    "lobster-pkg",
    "lobster-rst-report",
]

def _prune_stage_commands(package_dir):
    staged_root = "%s/lobster" % package_dir
    return [
        "find %s -type d -name __pycache__ -prune -exec rm -rf {} +" % staged_root,
        "find %s -type f \\( -name '*.pyc' -o -name '*.pyo' \\) -delete" % staged_root,
    ]

def _package_build_commands(package_name, spec):
    package_dir = "packages/%s" % package_name
    kind = spec["kind"]
    commands = ["rm -rf %s/lobster %s/build %s/dist %s/meta_dist" % (package_dir, package_dir, package_dir, package_dir)]

    if kind == "mono":
        commands.extend([
            "cp -R lobster %s/lobster" % package_dir,
        ])
        commands.extend(_prune_stage_commands(package_dir))
        commands.extend([
            "(cd %s && python3 -m build --wheel)" % package_dir,
        ])
        commands.extend(_prune_stage_commands(package_dir))
        commands.extend([
            "mv %s/dist %s/meta_dist" % (package_dir, package_dir),
        ])
        return commands

    commands.append("mkdir -p %s/lobster/tools" % package_dir)

    if kind == "core":
        commands.extend([
            "cp lobster/*.py %s/lobster" % package_dir,
            "cp -R lobster/common %s/lobster" % package_dir,
            "cp -R lobster/htmldoc %s/lobster" % package_dir,
            "cp lobster/tools/*.py %s/lobster/tools" % package_dir,
            "cp -R lobster/tools/core %s/lobster/tools" % package_dir,
        ])
    elif kind == "tool":
        commands.extend([
            "cp lobster/__init__.py %s/lobster" % package_dir,
            "cp -R lobster/common %s/lobster" % package_dir,
            "cp -R lobster/tools/%s %s/lobster/tools" % (spec["tool"], package_dir),
        ])
    elif kind == "meta":
        commands.extend([
            "cp lobster/__init__.py %s/lobster" % package_dir,
            "cp -R lobster/common %s/lobster" % package_dir,
        ])
    else:
        fail("unsupported package kind: %s" % kind)

    commands.extend(_prune_stage_commands(package_dir))
    commands.append("(cd %s && python3 -m build --wheel)" % package_dir)
    commands.extend(_prune_stage_commands(package_dir))
    return commands

def _clean_commands():
    commands = []
    for package_name in PACKAGE_ORDER:
        package_dir = "packages/%s" % package_name
        commands.extend([
            "rm -rf %s/lobster %s/dist %s/meta_dist %s/build" % (package_dir, package_dir, package_dir, package_dir),
            "find %s -maxdepth 1 -type d -name '*.egg-info' -exec rm -rf {} +" % package_dir,
        ])
    commands.append("rm -rf test_install test_install_monolithic test_install_monolithic_venv")
    return commands

def _pipeline_commands():
    commands = []
    for package_name in PACKAGE_ORDER:
        commands.extend(_package_build_commands(package_name, PACKAGE_SPECS[package_name]))

    split_wheels = " ".join(["packages/%s/dist/*.whl" % package_name for package_name in PACKAGE_ORDER[:-1]])
    mono_wheels = "packages/lobster-monolithic/meta_dist/*.whl"
    smoke_checks = "\n".join([
        "%s --version" % command
        for command in SMOKE_TEST_COMMANDS
    ])

    commands.extend([
        "rm -rf test_install test_install_monolithic test_install_monolithic_venv",
        "pip3 install --ignore-installed --prefix test_install %s" % split_wheels,
        "pip3 install --ignore-installed --prefix test_install_monolithic %s" % mono_wheels,
        "split_pkg=$(find test_install/lib -mindepth 2 -maxdepth 2 \\( -name site-packages -o -name dist-packages \\) | head -n 1)",
        "mono_pkg=$(find test_install_monolithic/lib -mindepth 2 -maxdepth 2 \\( -name site-packages -o -name dist-packages \\) | head -n 1)",
        "split_bin=test_install/bin; [[ -d $split_bin ]] || split_bin=test_install/local/bin",
        "mono_bin=test_install_monolithic/bin; [[ -d $mono_bin ]] || mono_bin=test_install_monolithic/local/bin",
        "diff -Naur \"$split_pkg/lobster\" \"$mono_pkg/lobster\" -x '*.pyc' -x '*pkg*' -x 'pkg/*'",
        "diff -Naur \"$split_bin\" \"$mono_bin\" -x '*pkg*' -x 'pkg/*'",
        "python3 -m venv test_install_monolithic_venv",
        ". test_install_monolithic_venv/bin/activate",
        "pip install --upgrade pip",
        "pip install %s" % mono_wheels,
        smoke_checks,
    ])
    return commands

def _emit_script(ctx, commands):
    script = ctx.actions.declare_file(ctx.label.name)
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        'cd "${BUILD_WORKSPACE_DIRECTORY:-$PWD}"',
    ]
    lines.extend(commands)
    ctx.actions.write(script, "\n".join(lines) + "\n", is_executable = True)
    return DefaultInfo(executable = script)

def _package_build_impl(ctx):
    return _emit_script(ctx, _package_build_commands(ctx.attr.package_name, ctx.attr.spec))

def _package_clean_impl(ctx):
    return _emit_script(ctx, _clean_commands())

def _package_pipeline_impl(ctx):
    return _emit_script(ctx, _pipeline_commands())

_package_build = rule(
    implementation = _package_build_impl,
    executable = True,
    attrs = {
        "package_name": attr.string(mandatory = True),
        "spec": attr.string_dict(mandatory = True),
    },
)

_package_clean = rule(
    implementation = _package_clean_impl,
    executable = True,
)

_package_pipeline = rule(
    implementation = _package_pipeline_impl,
    executable = True,
)

def package_build(name, package_name):
    _package_build(
        name = name,
        package_name = package_name,
        spec = PACKAGE_SPECS[package_name],
    )

def package_clean(name):
    _package_clean(name = name)

def package_pipeline(name):
    _package_pipeline(name = name)
