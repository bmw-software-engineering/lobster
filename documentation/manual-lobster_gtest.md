# Tracing to Googletests

## Setup and requirements

You will need to make available the
[lobster_gtest.h](../support/gtest/include/lobster_gtest.h) file to your build
environment. This file is in the public domain so you can include /
copy / rework it as you wish.

If you're using bazel then you can also use the included `BUILD` file
in that directory to make available a `lobster_gtest` library.

## Adding tags to tests

In your test you need to include `lobster_gtest.h` and then you can
write a single `LOBSTER_TRACE` macro. For example:

```C++
#include <gtest/gtest.h>
#include <lobster_gtest.h>

TEST(ImplicationTest, BasicTest)
{
  LOBSTER_TRACE("math.gt");
  EXPECT_TRUE(5 > 3);
}
```

Please note: only the last `LOBSTER_TRACE` will be used, if you want
to tag more than one requirement you need to provide a comma-separated
list, for example: `LOBSTER_TRACE("math.gt, math.truth");`.

Internally this works by using the RecordPropery functionality of
googletest.

## Creating lobster files

To extract tracing data, first execute your tests.

Then run the `lobster_gtest` tool, pointing it at the generated XML
artefacts. You can also provide a directory, in which case that
directory and all its subdirectories are searched for XML artefacts.

For example `lobster_gtest .` should find all your artefacts in most
cases.

You should also provide a `--out` file to write to. A more complete
command line might look like:

```sh
$ lobster_gtest . --out gtests.lobster
```

## Deriving Given/When/Then from test names

If your tests are named `[<Prefix>_]Given<X>[_When<Y>]_(Expect|Then)<Z>`, then
`lobster_gtest` can derive the record properties `Given`, `When` and `Then`
from the name instead of requiring a `RecordProperty` call in each test:

```sh
$ lobster_gtest . --out gtests.lobster --derive-gwt-from-test-name
```

For example `Stack_GivenEmptyStack_WhenPopCalled_ExpectError` adds

```text
:Given: empty stack
:When: pop called
:Then: error
```

* `<X>`, `<Y>` and `<Z>` are CamelCase words. They are converted to lower case
  words, e.g. `HTTPServer` gives `http server` and `Port80Open` gives
  `port 80 open`. A word is split before an upper case letter which follows a
  lower case letter or a digit, before a digit which follows a letter, and
  before the last upper case letter of a run of upper case letters if a lower
  case letter follows it. Acronyms with lower case letters inside, e.g. `URLs`
  or `IPv4`, are therefore split into `ur ls` and `i pv 4`. Write such
  acronyms in CamelCase, e.g. `Urls`.
* `<Prefix>` is a single alphanumeric word, e.g. the name of the unit under
  test. `_When<Y>` is optional.
* The whole name must match. For parameterized tests every `/` separated part of
  the name is tried, and the last matching part is used.
* If the test sets any of `Given`, `When` or `Then` itself (non-blank, ignoring
  letter case), then nothing is derived from its name, and a warning is printed
  to stderr. Blank properties count as not set.
* A test whose name does not match is not changed.

In Bazel set the attribute `derive_gwt_from_test_name = True` of `lobster_gtest`.

## Reports of other test frameworks

`lobster-gtest` reads GoogleTest XML reports only and ignores XML files in
which no test case has a `status` attribute, such as the JUnit XML reports of
pytest. To trace tests of other frameworks, or a test suite which mixes
frameworks, use [lobster-junit](manual-lobster_junit.md), which writes the same
items for GoogleTest reports.

## Example

The LOBSTER testsuite contains a working example:

* Bazel [BUILD](../tests_integration/projects/basic/BUILD.bazel) file to set up
* Test [test.cpp](../tests_integration/projects/basic/test.cpp) containing tracing tags
* Requrements [potato.trlc](../tests_integration/projects/basic/potato.trlc)
  containing tracing the requirements mentioned by the test
* [Makefile](../tests_integration/projects/basic/Makefile) gluing everything
  together. In the MakeFile search for target `gtests.lobster`

## Notes & Caveats

This LOBSTER tool works a bit differently:

* It's exctracting test data from the executed tests, so if a test is
  not compiled, there is no way for this system to locate it.
* You need to specify a comma separated list of items, whereas in all
  other tools you can just specify the tag comment more than
  once. This is because multiple calls to RecordProperty just
  overwrite instead of append.
