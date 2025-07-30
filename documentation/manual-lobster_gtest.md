# Tracing to Googletests

## Setup and requirements

You will need to make available the
[lobster_gtest.h](../support/gtest/lobster_gtest.h) file to your build
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

## Example

The LOBSTER testsuite contains a working example:

* Bazel [BUILD](../tests_integration/projects/basic/BUILD) file to set up
* Test [test.cpp](../tests_integration/projects/basic/test.cpp) containing tracing tags
* Requrements [potato.trlc](../tests_integration/projects/basic/potato.trlc)
  containing tracing the requirements mentioned by the test
* [Makefile](../tests_integration/projects/basic/Makefile) gluing everything
  together

## Notes & Caveats

This LOBSTER tool works a bit differently:

* It's exctracting test data from the executed tests, so if a test is
  not compiled, there is no way for this system to locate it.
* You need to specify a comma separated list of items, whereas in all
  other tools you can just specify the tag comment more than
  once. This is because multiple calls to RecordProperty just
  overwrite instead of append.
