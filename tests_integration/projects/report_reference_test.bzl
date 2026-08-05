load("//:lobster.bzl", "LobsterProvider")

def _lobster_reference_test_impl(ctx):
    lobster_config_substitutions = {}
    for input_target in ctx.attr.inputs:
        lobster_config_substitutions.update(input_target[LobsterProvider].lobster_input)

    lobster_config = ctx.actions.declare_file("{}_expanded_lobster.conf".format(ctx.attr.name))
    ctx.actions.expand_template(
        template = ctx.file.config,
        output = lobster_config,
        substitutions = lobster_config_substitutions,
    )

    lobster_report = ctx.actions.declare_file("{}_report.json".format(ctx.attr.name))

    report_command = """
set -euo pipefail

exec_root="$PWD"
tool_path="{tool}"
case "$tool_path" in
  /*) ;;
  *) tool_path="$exec_root/$tool_path" ;;
esac

config_rel="$1"
out_rel="$2"
shift 2

stage_dir="$(mktemp -d)"
trap 'rm -rf "$stage_dir"' EXIT

cp "$config_rel" "$stage_dir/lobster.conf"

while [ "$#" -gt 0 ]; do
  src_rel="$1"
  src_base="$2"
  shift 2
    src_path="$src_rel"
    case "$src_path" in
        /*) ;;
        *) src_path="$exec_root/$src_path" ;;
    esac
    if [ ! -f "$src_path" ]; then
        echo "missing staged input: $src_base from $src_path" >&2
        exit 1
    fi
    cp "$src_path" "$stage_dir/$src_base"
done

cd "$stage_dir"
"$tool_path" --lobster-config lobster.conf --out "$exec_root/$out_rel"
""".format(
        tool = ctx.executable._lobster_report.path,
    )

    report_args = ctx.actions.args()
    report_args.add(lobster_config.path)
    report_args.add(lobster_report.path)
    for input_file in ctx.files.inputs:
        report_args.add(input_file.path)
        report_args.add(input_file.basename)

    ctx.actions.run_shell(
        command = report_command,
        inputs = ctx.files.inputs + [lobster_config],
        outputs = [lobster_report],
        arguments = [report_args],
        tools = [ctx.executable._lobster_report],
        progress_message = "lobster-report {}".format(lobster_report.path),
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

lobster_reference_test = rule(
    implementation = _lobster_reference_test_impl,
    attrs = {
        "config": attr.label(
            allow_single_file = True,
            mandatory = True,
        ),
        "inputs": attr.label_list(
            providers = [LobsterProvider],
            mandatory = True,
        ),
        "reference": attr.label(
            allow_single_file = True,
            mandatory = True,
        ),
        "_lobster_report": attr.label(
            default = "//:lobster-report",
            executable = True,
            cfg = "exec",
        ),
    },
    test = True,
)
