load("@trlc//:trlc.bzl", "TrlcProviderInfo")
load("//bazel:providers.bzl", "LobsterProvider")

def _lobster_trlc_subrule_impl(ctx, requirements, config, _lobster_trlc):
    lobster_trlc_trace = ctx.actions.declare_file(ctx.label.name + ".lobster")

    args = ctx.actions.args()
    args.add_all(["--config", config.path])
    args.add_all(["--out", lobster_trlc_trace.path])

    ctx.actions.run(
        executable = _lobster_trlc,
        inputs = requirements + [config],
        outputs = [lobster_trlc_trace],
        arguments = [args],
        progress_message = "lobster-trlc {}".format(lobster_trlc_trace.path),
    )

    return [
        lobster_trlc_trace,
        LobsterProvider(lobster_input = {lobster_trlc_trace.basename: lobster_trlc_trace.path}),
    ]

subrule_lobster_trlc = subrule(
    implementation = _lobster_trlc_subrule_impl,
    attrs = {
        "_lobster_trlc": attr.label(
            default = "//:lobster-trlc",
            executable = True,
            cfg = "exec",
        ),
    },
)

def _lobster_trlc_impl(ctx):
    lobster_trlc_trace, lobster_provider = subrule_lobster_trlc(ctx.files.requirements, ctx.file.config)
    return [DefaultInfo(files = depset([lobster_trlc_trace])), lobster_provider]

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
    },
    subrules = [subrule_lobster_trlc],
)
