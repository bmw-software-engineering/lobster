"""Runs lobster-trlc and lobster-report like the project Makefiles and diffs against a reference.

This is a py_test and not a generated shell script, so it also runs on Windows.
"""

load("@rules_python//python:defs.bzl", "py_test")

def lobster_integration_test(name, srcs, trlc_configs, config, reference, **kwargs):
    """Runs the lobster tools on a project and tests the report against a reference.

    Args:
        name: Name of the test target.
        srcs: TRLC and RSL files.
        trlc_configs: lobster-trlc config mapped to the .lobster file it produces.
        config: lobster-report config, staged as lobster.conf.
        reference: The expected report.
        **kwargs: Forwarded to the py_test.
    """
    runner = Label("//tests_integration/projects:run_integration_test.py")
    args = ["--config", "$(rlocationpath {})".format(config)]
    args += ["--reference", "$(rlocationpath {})".format(reference)]
    for src in srcs:
        args += ["--src", "$(rlocationpath {})".format(src)]
    for trlc_config, output in trlc_configs.items():
        args += ["--trlc", "$(rlocationpath {})={}".format(trlc_config, output)]

    py_test(
        name = name,
        srcs = [runner],
        main = runner,
        args = args,
        data = srcs + trlc_configs.keys() + [config, reference],
        deps = [
            "//lobster/tools/core/report",
            "//lobster/tools/trlc",
            "@rules_python//python/runfiles",
        ],
        **kwargs
    )
