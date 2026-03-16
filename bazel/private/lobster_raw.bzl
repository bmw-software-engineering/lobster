load("//bazel:providers.bzl", "LobsterProvider")

def _lobster_raw_impl(ctx):
    name = "{}.lobster".format(ctx.attr.name)

    return [
        DefaultInfo(files = depset([ctx.file.src])),
        LobsterProvider(lobster_input = {name: ctx.file.src.path}),
    ]

lobster_raw = rule(
    implementation = _lobster_raw_impl,
    attrs = {
        "src": attr.label(
            allow_single_file = [".lobster"],
            mandatory = True,
        ),
    },
)
