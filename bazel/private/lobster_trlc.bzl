load("@trlc//:trlc.bzl", "TrlcProviderInfo")
load("//bazel:providers.bzl", "LobsterProvider")

def _lobster_trlc_subrule_impl(ctx, requirements, config, _lobster_trlc):
    lobster_trlc_trace = ctx.actions.declare_file(ctx.label.name + ".lobster")

    package_dir = ctx.label.package
    config_base = config.basename
    command = """
set -euo pipefail
exec_root="$PWD"
tool_path="{tool}"
case "$tool_path" in
    /*) ;;
    *) tool_path="$exec_root/$tool_path" ;;
esac
out_path="{out}"
case "$out_path" in
    /*) ;;
    *) out_path="$exec_root/$out_path" ;;
esac
cd {package_dir}
"$tool_path" --config {config_base} --out "$out_path"
""".format(
        package_dir = package_dir,
        tool = _lobster_trlc.executable.path,
        config_base = config_base,
        out = lobster_trlc_trace.path,
    )

    ctx.actions.run_shell(
        command = command,
        inputs = requirements + [config],
        outputs = [lobster_trlc_trace],
        tools = [_lobster_trlc],
        progress_message = "lobster-trlc {}".format(lobster_trlc_trace.path),
    )

    return [
        lobster_trlc_trace,
        # Keep config substitutions one-to-one with Make behavior by preserving
        # plain basenames in lobster.conf source fields.
        LobsterProvider(lobster_input = {lobster_trlc_trace.basename: lobster_trlc_trace.basename}),
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
