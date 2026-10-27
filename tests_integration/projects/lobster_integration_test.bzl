"""Test-only rule: runs lobster-trlc and lobster-report like the project Makefiles and diffs against a reference."""

def _sh(value):
    return "'" + value.replace("'", "'\\''") + "'"

def _lobster_integration_test_impl(ctx):
    trlc_configs = [(target.files.to_list()[0], out) for target, out in ctx.attr.trlc_configs.items()]

    # Files are staged flat, so the tools see the same relative paths as in the Makefile flow.
    staged = ctx.files.srcs + [config for config, _ in trlc_configs]
    names = {}
    for f in staged:
        if f.basename in names:
            fail("{}: duplicate staged file name {}".format(ctx.label, f.basename))
        names[f.basename] = True

    lobster_report = ctx.actions.declare_file("{}_report.json".format(ctx.attr.name))

    lines = [
        "set -euo pipefail",
        'exec_root="$PWD"',
        'stage="$(mktemp -d)"',
        "trap 'rm -rf \"$stage\"' EXIT",
    ]
    for f in staged:
        lines.append('cp {} "$stage"/{}'.format(_sh(f.path), _sh(f.basename)))
    lines.append('cp {} "$stage/lobster.conf"'.format(_sh(ctx.file.config.path)))
    lines.append('cd "$stage"')
    for config, out in trlc_configs:
        lines.append('"$exec_root"/{} --config {} --out {}'.format(
            _sh(ctx.executable._lobster_trlc.path),
            _sh(config.basename),
            _sh(out),
        ))
    lines.append('"$exec_root"/{} --lobster-config lobster.conf --out "$exec_root"/{}'.format(
        _sh(ctx.executable._lobster_report.path),
        _sh(lobster_report.path),
    ))

    ctx.actions.run_shell(
        command = "\n".join(lines),
        inputs = staged + [ctx.file.config],
        outputs = [lobster_report],
        tools = [ctx.executable._lobster_trlc, ctx.executable._lobster_report],
        progress_message = "lobster integration {}".format(lobster_report.path),
    )

    test_executable = ctx.actions.declare_file("{}_reference_test.sh".format(ctx.attr.name))
    script = """#!/usr/bin/env bash
set -euo pipefail

report="${{TEST_SRCDIR}}/${{TEST_WORKSPACE}}/{report}"
reference="${{TEST_SRCDIR}}/${{TEST_WORKSPACE}}/{reference}"

diff -u "$report" "$reference"
""".format(
        report = lobster_report.short_path,
        reference = ctx.file.reference.short_path,
    )
    ctx.actions.write(
        output = test_executable,
        content = script,
        is_executable = True,
    )

    return [DefaultInfo(
        executable = test_executable,
        files = depset([lobster_report]),
        runfiles = ctx.runfiles(files = [lobster_report, ctx.file.reference]),
    )]

lobster_integration_test = rule(
    implementation = _lobster_integration_test_impl,
    attrs = {
        "srcs": attr.label_list(
            allow_files = True,
            mandatory = True,
            doc = "TRLC and RSL files.",
        ),
        "trlc_configs": attr.label_keyed_string_dict(
            allow_files = True,
            mandatory = True,
            doc = "lobster-trlc config mapped to the .lobster file it produces.",
        ),
        "config": attr.label(
            allow_single_file = True,
            mandatory = True,
            doc = "lobster-report config, staged as lobster.conf.",
        ),
        "reference": attr.label(
            allow_single_file = True,
            mandatory = True,
        ),
        "_lobster_trlc": attr.label(
            default = "//:lobster-trlc",
            executable = True,
            cfg = "exec",
        ),
        "_lobster_report": attr.label(
            default = "//:lobster-report",
            executable = True,
            cfg = "exec",
        ),
    },
    test = True,
)
