"""
Generates the XML report of a test target, for any test framework.

The test is run as part of the build, and the generated XML report is made
available as a build output. The test runs with its runfiles and the
environment of its target (attribute "env"). It is given no command line
arguments; instead, the location of the report is passed in the environment,
following the protocol of "bazel test":

* XML_OUTPUT_FILE: read by googletest >= 1.10 and by tests which pass
  "--junitxml=$XML_OUTPUT_FILE" to pytest
* GTEST_OUTPUT: read by older googletest versions
* GTEST_BRIEF: reduces the console output of googletest

ATTENTION:
This rule will not rerun tests unless this rule was modified or the test
executable was modified. E.g. Bazel arguments like "--runs_per_test" do not
have an effect on this rule.
"""

def _test_report_subrule_impl(ctx, name, test):
    xml = ctx.actions.declare_file("{}.xml".format(name))

    env = {}
    if RunEnvironmentInfo in test:
        env.update(test[RunEnvironmentInfo].environment)
    env.update({
        "GTEST_BRIEF": "1",
        "GTEST_OUTPUT": "xml:{}".format(xml.path),
        "XML_OUTPUT_FILE": xml.path,
    })

    ctx.actions.run(
        outputs = [xml],
        # A FilesToRunProvider, unlike a File, makes Bazel provide the runfiles
        # of the test, which launcher-based tests such as py_test need.
        executable = test[DefaultInfo].files_to_run,
        env = env,
        mnemonic = "TestReport",
        progress_message = "Running {} for its test report".format(test.label),
    )

    return xml

subrule_test_report = subrule(
    implementation = _test_report_subrule_impl,
)

def _test_report_impl(ctx):
    xml = subrule_test_report(ctx.label.name, ctx.attr.test)
    return [DefaultInfo(files = depset([xml]))]

test_report = rule(
    implementation = _test_report_impl,
    attrs = {
        "test": attr.label(
            mandatory = True,
            executable = True,
            cfg = "target",
            doc = "The test target. It must write a JUnit XML report to the " +
                  "file named by the environment variable XML_OUTPUT_FILE.",
        ),
    },
    subrules = [subrule_test_report],
)
