load("//bazel:providers.bzl", _LobsterProvider = "LobsterProvider")
load("//bazel/private:lobster_test.bzl", _lobster_test = "lobster_test")
load("//bazel/private:lobster_trlc.bzl", _lobster_trlc = "lobster_trlc")
load("//bazel/private:lobster_raw.bzl", _lobster_raw = "lobster_raw")

# Re-export LobsterProvider so it can be loaded from this file
LobsterProvider = _LobsterProvider

def lobster_test(**kwargs):
    _lobster_test(**kwargs)

def lobster_trlc(**kwargs):
    _lobster_trlc(**kwargs)

def lobster_raw(**kwargs):
    _lobster_raw(**kwargs)

def _lobster_gtest(ctx):
    lobster_gtest_trace = ctx.actions.declare_file(ctx.attr.name + ".lobster")

    args = ctx.actions.args()
    args.add_all(["--out", lobster_gtest_trace.path])
    args.add(".")

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
