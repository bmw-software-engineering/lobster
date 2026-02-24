load("//bazel:providers.bzl", "LobsterProvider")

def _lobster_gtest_subrule_impl(ctx, tests, _lobster_gtest):
    lobster_gtest_trace = ctx.actions.declare_file(ctx.label.name + ".lobster")

    args = ctx.actions.args()
    args.add_all(["--out", lobster_gtest_trace.path])
    args.add(".")

    ctx.actions.run(
        executable = _lobster_gtest,
        inputs = tests,
        outputs = [lobster_gtest_trace],
        arguments = [args],
        progress_message = "lobster-gtest {}".format(lobster_gtest_trace.path),
    )

    return [
        lobster_gtest_trace,
        LobsterProvider(lobster_input = {lobster_gtest_trace.basename: lobster_gtest_trace.path}),
    ]

subrule_lobster_gtest = subrule(
    implementation = _lobster_gtest_subrule_impl,
    attrs = {
        "_lobster_gtest": attr.label(
            default = "//:lobster-gtest",
            executable = True,
            cfg = "exec",
        ),
    },
)

def _lobster_gtest(ctx):
    lobster_gtest_trace, lobster_provider = subrule_lobster_gtest(ctx.files.tests)
    return [DefaultInfo(files = depset([lobster_gtest_trace])), lobster_provider]

lobster_gtest = rule(
    implementation = _lobster_gtest,
    attrs = {
        "tests": attr.label_list(
            allow_empty = False,
            mandatory = True,
        ),
    },
    subrules = [subrule_lobster_gtest],
)
