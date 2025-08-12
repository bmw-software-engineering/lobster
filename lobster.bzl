load("@trlc//:trlc.bzl", "TrlcProviderInfo")

LobsterProvider = provider(
    fields = {
        "lobster_input": "ABC",
    },
)

def _lobster_test_impl(ctx):
    lobster_report = ctx.actions.declare_file(ctx.attr.name + "_report.json")

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

    args = ctx.actions.args()
    args.add_all(["--lobster-config", lobster_config.path])
    args.add_all(["--out", lobster_report.path])

    ctx.actions.run(
        executable = ctx.executable._lobster_report,
        inputs = depset(ctx.files.inputs + [lobster_config]),
        outputs = [lobster_report],
        arguments = [args],
        progress_message = "lobster-report {}".format(lobster_report.path),
    )
    ###############

    lobster_html_report = ctx.actions.declare_file("{}_report.html".format(ctx.attr.name))

    args = ctx.actions.args()
    args.add(lobster_report.path)
    args.add_all(["--out", lobster_html_report.path])

    ctx.actions.run(
        executable = ctx.executable._lobster_html_report,
        inputs = [lobster_report],
        outputs = [lobster_html_report],
        arguments = [args],
        progress_message = "lobster-html-report {}".format(lobster_html_report.path),
    )

    ###############

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

_lobster_test = rule(
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
        "source_filter": attr.string_list(
            doc = "List of strings, which are used to exclude source and test files if they start with any of the strings.",
            default = [],
        ),
        "_lobster_report": attr.label(
            default = "//:lobster-report",
            executable = True,
            cfg = "exec",
        ),
        "_lobster_html_report": attr.label(
            default = "//:lobster-html-report",
            executable = True,
            cfg = "exec",
        ),
        "_lobster_ci_report": attr.label(
            default = "//:lobster-ci-report",
            executable = True,
            cfg = "exec",
        ),
    },
    test = True,
)

def lobster_test(**kwargs):
    _lobster_test(**kwargs)

def _lobster_trlc_impl(ctx):
    lobster_trlc_trace = ctx.actions.declare_file(ctx.attr.name + ".lobster")

    args = ctx.actions.args()
    args.add_all(["--config", ctx.file.config.path])
    args.add_all(["--out", lobster_trlc_trace.path])

    ctx.actions.run(
        executable = ctx.executable._lobster_trlc,
        inputs = ctx.files.requirements + [ctx.file.config],
        outputs = [lobster_trlc_trace],
        arguments = [args],
        progress_message = "lobster-trlc {}".format(lobster_trlc_trace.path),
    )

    return [
        DefaultInfo(files = depset([lobster_trlc_trace])),
        LobsterProvider(lobster_input = {lobster_trlc_trace.basename: lobster_trlc_trace.path}),
    ]

_lobster_trlc = rule(
    implementation = _lobster_trlc_impl,
    attrs = {
        "requirements": attr.label_list(
            doc = "Targets that define requirements in the form of TRLC files.",
            providers = [TrlcProviderInfo],
            mandatory = True,
        ),
        "config": attr.label(
            allow_single_file = True,
            mandatory = True,
        ),
        "_lobster_trlc": attr.label(
            default = "//:lobster-trlc",
            executable = True,
            cfg = "exec",
        ),
    },
)

def lobster_trlc(**kwargs):
    _lobster_trlc(**kwargs)

def _lobster_raw_impl(ctx):
    name = "{}.lobster".format(ctx.attr.name)

    return [
        DefaultInfo(files = depset([ctx.file.src])),
        LobsterProvider(lobster_input = {name: ctx.file.src.path}),
    ]

_lobster_raw = rule(
    implementation = _lobster_raw_impl,
    attrs = {
        "src": attr.label(
            allow_single_file = [".lobster"],
            mandatory = True,
        ),
    },
)

def lobster_raw(**kwargs):
    _lobster_raw(**kwargs)

def _lobster_gtest(ctx):
    lobster_gtest_trace = ctx.actions.declare_file(ctx.attr.name + ".lobster")

    args = ctx.actions.args()
    args.add_all(["--out", lobster_gtest_trace.path])
    args.add(".")

    print(ctx.attr.tests[0][OutputGroupInfo])

    ctx.actions.run(
        executable = ctx.executable._lobster_gtest,
        inputs = ctx.files.tests,
        outputs = [lobster_gtest_trace],
        arguments = [args],
        progress_message = "lobster-gtest {}".format(lobster_gtest_trace.path),
    )

    return [
        DefaultInfo(files = depset([lobster_gtest_trace])),
        LobsterProvider(lobster_input = {lobster_gtest_trace.basename: lobster_gtest_trace.path}),
    ]

lobster_gtest = rule(
    implementation = _lobster_gtest,
    attrs = {
        "tests": attr.label_list(
            allow_empty = False,
            mandatory = True,
        ),
        "_lobster_gtest": attr.label(
            default = "//:lobster-gtest",
            executable = True,
            cfg = "exec",
        ),
    },
)
