# Tracing to JUnit XML test reports (pytest, GoogleTest, ...)

`lobster-junit` extracts tracing data from the JUnit XML reports which most
test frameworks write, for example pytest (`--junitxml`) or GoogleTest
(`--gtest_output=xml`). It detects the dialect of every report and reads it
accordingly, so a test suite which mixes test frameworks is traced with one
call.

For GoogleTest reports, `lobster-junit` writes exactly the items which
[lobster-gtest](manual-lobster_gtest.md) writes.

## Adding tags to tests

A test case links to requirements through the property `lobster-tracing`.
Its value lists the requirements, separated by commas, whitespace or both.
A requirement can be pinned to a version with `@<version>`, e.g.
`math.gt@2`.

In pytest, record the property with the `record_property` fixture:

```python
def test_greater_than(record_property):
    record_property("lobster-tracing", "math.gt, math.truth")
    assert 5 > 3
```

pytest writes the file and the line of a test only with the JUnit family
`xunit1`, so run it with `-o junit_family=xunit1` (or set `junit_family =
xunit1` in its configuration) to get links to the test source:

```sh
$ pytest -o junit_family=xunit1 --junitxml=pytest_report.xml
```

For GoogleTest see [lobster-gtest](manual-lobster_gtest.md#adding-tags-to-tests).
Other test frameworks write the property in the same way, as a `<property>` of
the `<testcase>` element.

Further properties of a test case:

* `lobster-tracing-file` and `lobster-tracing-line` set the location of the
  test, if the one written by the test framework is not suitable.
* Every other property is added to the item text as a line `:<Name>: <value>`,
  e.g. `given`, `when` and `then`.

## Creating lobster files

Run your tests, then point `lobster-junit` at the reports, or at directories
which are searched for `*.xml` files:

```sh
$ lobster-junit pytest_report.xml gtest_report.xml --out tests.lobster
```

XML files which are not test reports are ignored.

## Bazel

Load the rules from `@lobster//:lobster.bzl`:

* `test_report` runs a test target as part of the build and provides its XML
  report. It works for any test framework: the test gets no command line
  arguments, but finds the location of the report in the environment variable
  `XML_OUTPUT_FILE`, as under `bazel test`. googletest reads it by itself, a
  pytest test passes `--junitxml=$XML_OUTPUT_FILE` to `pytest.main()`. The test
  runs with its runfiles and the environment of its target (attribute `env`).
* `lobster_junit` runs `lobster-junit` on the reports.

```starlark
load("@lobster//:lobster.bzl", "lobster_junit", "test_report")

test_report(
    name = "cc_report",
    testonly = True,
    test = ":my_cc_test",
)

test_report(
    name = "py_report",
    testonly = True,
    test = ":my_py_test",
)

lobster_junit(
    name = "tests",
    testonly = True,
    derive_gwt_from_test_name = True,
    tests = [":cc_report", ":py_report"],
)
```

Rules which run tests themselves can use the subrules `subrule_test_report`
and `subrule_lobster_junit`. A working example is the integration test project
[tests_integration/projects/junit](../tests_integration/projects/junit/BUILD.bazel).

## Report dialects

| Dialect | Detected by | Item tag | Framework |
| --- | --- | --- | --- |
| GoogleTest | root `<testsuites>` and a `<testcase>` with attribute `status` | `gtest <suite>:<test>` | `GoogleTest` |
| pytest | root `<testsuites>`/`<testsuite>` whose name starts with `pytest` | `junit <classname>:<name>` | `pytest` |
| JUnit | any other root `<testsuites>`/`<testsuite>` | `junit <classname>:<name>` | `JUnit` |

For pytest and JUnit reports:

* Every `<testcase>` of every `<testsuite>`, also of nested ones, becomes an
  item. Without a `classname`, the name of the test suite is used instead.
* The status is `not run` for a test case with a `<skipped>` element, `fail`
  for one with a `<failure>` or `<error>` element, and `ok` otherwise.
* pytest reports the 0-based line of a test function; `lobster-junit` writes
  the 1-based line.

## Deriving Given/When/Then from test names

With `--derive-gwt-from-test-name`, Given, When and Then are derived from test
names which follow the convention described for
[lobster-gtest](manual-lobster_gtest.md#deriving-givenwhenthen-from-test-names).
For pytest, `test` serves as the prefix, and the parameters of a parametrized
test are ignored:

```python
@pytest.mark.parametrize("value", [1, 2])
def test_GivenValue_ExpectPositive(value, record_property):
    record_property("lobster-tracing", "math.positive")
    assert value > 0
```

adds `:Given: value` and `:Then: positive` to the items of both
`test_GivenValue_ExpectPositive[1]` and `test_GivenValue_ExpectPositive[2]`.

## Notes & Caveats

* `lobster-junit` extracts data from executed tests. A test which is not run
  does not appear in the report.
* A `lobster-tracing` property recorded several times adds all its
  requirements. For every other property, the last value is used.
