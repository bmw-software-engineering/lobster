load("//bazel:providers.bzl", "LobsterProvider")

def _lobster_report_subrule_impl(ctx, inputs, lobster_config, _lobster_report):
    lobster_report = ctx.actions.declare_file(ctx.label.name + "_report.json")

    args = ctx.actions.args()
    args.add_all(["--lobster-config", lobster_config.path])
    args.add_all(["--out", lobster_report.path])

    ctx.actions.run(
        executable = _lobster_report,
        inputs = depset(inputs + [lobster_config]),
        outputs = [lobster_report],
        arguments = [args],
        progress_message = "lobster-report {}".format(lobster_report.path),
    )

    return lobster_report

subrule_lobster_report = subrule(
    implementation = _lobster_report_subrule_impl,
    attrs = {
        "_lobster_report": attr.label(
            default = "//:lobster-report",
            executable = True,
            cfg = "exec",
        ),
    },
)

def _lobster_html_report_subrule_impl(ctx, lobster_report, _lobster_html_report):
    lobster_html_report = ctx.actions.declare_file("{}_report.html".format(ctx.label.name))

    args = ctx.actions.args()
    args.add(lobster_report.path)
    args.add_all(["--out", lobster_html_report.path])

    ctx.actions.run(
        executable = _lobster_html_report,
        inputs = [lobster_report],
        outputs = [lobster_html_report],
        arguments = [args],
        progress_message = "lobster-html-report {}".format(lobster_html_report.path),
    )

    return lobster_html_report

subrule_lobster_html_report = subrule(
    implementation = _lobster_html_report_subrule_impl,
    attrs = {
        "_lobster_html_report": attr.label(
            default = "//:lobster-html-report",
            executable = True,
            cfg = "exec",
        ),
    },
)

def _lobster_test_impl(ctx):
    lobster_config_substitutions = {}
    for input_config in ctx.attr.inputs:
        lobster_config_substitutions.update(input_config[LobsterProvider].lobster_input)

    # We have to adjust the paths from the config, with the paths used by Bazel
    lobster_config = ctx.actions.declare_file("{}_expanded_lobster.conf".format(ctx.attr.name))
    ctx.actions.expand_template(
        template = ctx.file.config,
        output = lobster_config,
        substitutions = lobster_config_substitutions,
    )

    lobster_report = subrule_lobster_report(ctx.files.inputs, lobster_config)
    lobster_html_report = subrule_lobster_html_report(lobster_report)

    test_executable = ctx.actions.declare_file("{}_lobster_ci_test_executable".format(ctx.attr.name))
    command = "set -o pipefail; {} {}".format(ctx.executable._lobster_ci_report.short_path, lobster_report.short_path)

    ctx.actions.write(
        output = test_executable,
        content = command,
    )

    return [DefaultInfo(
        runfiles = ctx.runfiles(
            files = [
                ctx.executable._lobster_ci_report,
                lobster_report,
            ],
        ).merge(ctx.attr._lobster_ci_report[DefaultInfo].default_runfiles),
        files = depset([lobster_report, lobster_html_report]),
        executable = test_executable,
    )]

lobster_test = rule(
    implementation = _lobster_test_impl,
    attrs = {
        "inputs": attr.label_list(
            providers = [LobsterProvider],
            mandatory = True,
        ),
        "config": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "_lobster_ci_report": attr.label(
            default = "//:lobster-ci-report",
            executable = True,
            cfg = "exec",
        ),
    },
    test = True,
    subrules = [subrule_lobster_report, subrule_lobster_html_report],
)
