"""
Generates a googletest report based on a test executable.
The tests are run as part of the build, and the generated XML report is made available as a build output.

ATTENTION:
This rule will not rerun tests unless this rule was modified or the test executable was modified.
E.g. Bazel arguments like "--runs_per_test" do not have an effect on this rule.

_RULE_ATTRS = {
    # In order for args expansion to work in bazel for an executable rule
    # the attributes must be one of: "srcs", "deps", "data" or "tools".
    # See Bazel's LocationExpander implementation, these attribute names
    # are hardcoded.
    "data": attr.label_list(
        allow_files = True,
    ),
    "deps": attr.label_list(
        allow_files = True,
    ),
    "env": attr.string_dict(),
    "executable": attr.label(
        allow_files = True,
        cfg = "target",
        executable = True,
        mandatory = True,
    ),
}

def _gtest_report_subrule_impl(ctx, name, executable, inputs, suppress_stdout = False):
    link = ctx.actions.declare_file(name + "_runner")
    xml = ctx.actions.declare_file("{}_test.xml".format(name))

    ctx.actions.symlink(
        output = link,
        target_file = executable,
        is_executable = True,
    )

    args = ctx.actions.args()
    args.add("--gtest_output=xml:{}".format(xml.path))

    if suppress_stdout:
        ctx.actions.run_shell(
            outputs = [xml],
            inputs = depset([link, executable], transitive = [inputs]),
            arguments = [args],
            command = '"{}" "$@" >/dev/null'.format(link.path),
        )
    else:
        ctx.actions.run(
            outputs = [xml],
            inputs = depset([executable], transitive = [inputs]),
            arguments = [args],
            executable = link,
        )

    return xml

subrule_gtest_report = subrule(
    implementation = _gtest_report_subrule_impl,
)

def _gtest_report_impl(ctx):
    all_inputs = depset(
        ctx.files.data + ctx.files.deps,
        transitive = [ctx.attr.executable.default_runfiles.files] +
                     [dataf.default_runfiles.files for dataf in ctx.attr.data] +
                     [dataf.data_runfiles.files for dataf in ctx.attr.data],
    )
    xml = subrule_gtest_report(ctx.label.name, ctx.executable.executable, all_inputs)
    return [DefaultInfo(files = depset([xml]))]

gtest_report = rule(
    implementation = _gtest_report_impl,
    attrs = _RULE_ATTRS,
    subrules = [subrule_gtest_report],
)
