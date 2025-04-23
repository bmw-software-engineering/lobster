# Tracing to C/C++ tests

## Setup and requirements

You will need a C/C++ file or a directory containing these files.
* Note: The tool also supports a combination of files and folders.

C/C++ files should have one of these extensions to be evaluated by this tool: `.cpp`, `.cc`, `.c` or `.h`

## Preparing C/C++ test documentation with requirements
The test functions should be specified with one the following `macros`: 
        `TEST`,
        `TEST_P`,
        `TEST_F`,
        `TYPED_TEST`,
        `TYPED_TEST_P`,
        `TYPED_TEST_SUITE`,
        `TEST_P_INSTANCE` or
        `TEST_F_INSTANCE`

In your test you need to also add documentation. For example:

```C++
/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(ImplicationTest, BasicTest) {}
```


## Notes:

* Each test can have multiple test-tags defined in the documentation part.
* Test-tags can be used multiple times in the test documentation and can be written on multiple lines

* These can be simply defined with `/** Test-tags */` or `/// Test-tags` format. 

* Test-tags can be separated by commas or spaces.

* Note: The `markers` shall be exactly close to the test functions (without any empty lines)


```C++
/**
 * @requirement CB-#0815, CB-#0816
 */
TEST(ImplicationTest, BasicTest) {}
```

```C++
///
/// @requiredby FOO0::BAR0
///
TEST(ImplicationTest, BasicTest) {}
```
The regex used for each test-tag is as follows:

@requirement
: ```r"(CB-#\d+)"```
: ```r"({provided codebeamer-url in YAML config-file}(?P<number>\d+))"```

@requiredby
: ```r"(\w*::\w+)"```

@defect
: ```r"(CB-#\d+)|(OCT-#\d+)"```


## Preparing cpptest YAML config-file

You have to provide a YAML config-file which determines which `markers` should be extracted in which output-files.
The expected `kind` for each output-file should also be specified.

In addition, you have to provide the `codebeamer-url`:

```cpptest-config.yaml
output:
  unit_tests.lobster:
    markers: ["@requirement"]
    kind: req

  components_tests.lobster:
    markers: ["@requiredby", "@requirement"]
    kind: imp

codebeamer_url: "https://codebeamer.example.com/cb"
 ```

* Note: Orphan tests, that do not match any configured `markers`, will be written into all defined outputs.
 Be aware these tests do not have any references.


## Creating lobster files

Run the `lobster_cpptest` tool, pointing it to one or more C/C++ files, or a directory containing one or more C/C++ files. 

For example `lobster_cpptest .` should find all your C/C++ files in the root directory.

Make sure to provide the updated YAML config file using --config.
A more complete command line might look like:

```sh
$ lobster-cpptest . --config cpptest-config.yaml
```

## Example

The LOBSTER unit tests contains a working example:

* Test [test_case.cpp](../test-unit/lobster-cpptest/data/test_case.cpp) containing requirement tags

## Notes & Caveats
* This tool supports these `markers`: '@requirement', '@requiredby' and '@defect'
* This tool supports these `kind`: 'req', 'imp' and 'act'
* YAML configuration format is now required instead of the previous JSON-like .config format
