load("@trlc//:trlc.bzl", "TrlcProviderInfo")

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

lobster_trlc = rule(
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
