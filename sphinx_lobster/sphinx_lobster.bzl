"""Bazel rule to expose the merged lobster file from a sphinx lobster build.

The sphinx lobster builder (``-b lobster``) writes one ``.json`` file per RST
document and, in its ``finish()`` hook, produces ``_merged.lobster`` inside the
output directory.  ``sphinx_lobster`` exposes that path via
``LobsterProvider`` so it can be used as an input to ``lobster_test`` without
any additional copy or merge action — the sphinx build action itself is the
only step needed.
"""

load("@lobster//:lobster.bzl", "LobsterProvider")

def _sphinx_lobster_impl(ctx):
    lobster_dirs = ctx.attr.sphinx_docs[OutputGroupInfo].lobster.to_list()
    if not lobster_dirs:
        fail(
            "sphinx_docs target '{}' has no 'lobster' output group. ".format(
                ctx.attr.sphinx_docs.label,
            ) + "Make sure 'lobster' is listed in the sphinx_docs `formats` attribute.",
        )

    lobster_dir = lobster_dirs[0]

    # LobsterBuilder.finish() writes _merged.lobster into the sphinx output
    # directory.  The directory is already an action output of the sphinx build
    # and will be available in any downstream action sandbox, so we can
    # reference the file directly without an extra copy.
    # NOTE: The filename "_merged.lobster" is also hardcoded in the Python
    # plugin at /sphinx/sphinx_lobster_builder.py (LobsterBuilder.finish).
    # Both names must stay in sync.
    merged_path = lobster_dir.path + "/_merged.lobster"

    return [
        DefaultInfo(files = depset([lobster_dir])),
        LobsterProvider(lobster_input = {ctx.label.name + ".lobster": merged_path}),
    ]

sphinx_lobster = rule(
    implementation = _sphinx_lobster_impl,
    doc = """Wrap a sphinx lobster build as a LobsterProvider.

    Takes the 'lobster' output group of a ``sphinx_docs`` target and provides
    the ``_merged.lobster`` file (written by ``LobsterBuilder.finish()``) via
    ``LobsterProvider`` for use with ``lobster_test``.  No additional action
    is performed; the sphinx build itself is sufficient.
    """,
    attrs = {
        "sphinx_docs": attr.label(
            doc = "A sphinx_docs target that has 'lobster' in its formats list.",
            providers = [OutputGroupInfo],
            mandatory = True,
        ),
    },
)
