# Tracing to C++ tests

## Setup and requirements

You will need a C++ file or a directory containing these files.

Note: The tool also supports a combination of files and folders.

C++ files should have one of these extensions to be evaluated by this tool: `.cpp`, `.cc`, `.c` or `.h`

## Preparing C++ test documentation with requirements
The test functions must be specified with one the following fixture names: 
`TEST`,
`TEST_P`,
`TEST_F`,
`TYPED_TEST`,
`TYPED_TEST_P`,
`TYPED_TEST_SUITE`,
`TEST_P_INSTANCE` or
`TEST_F_INSTANCE`.
Currently these names are hardcoded and are not configurable.

This tool has been developed to support C++, where C was not in the focus.
You can use it for C as well, if your test functions are all defined using macros
that use the above names, and hence mimic the C++ style.

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
    markers: ["@requirement"]
    kind: imp

codebeamer_url: "https://codebeamer.example.com/cb"
 ```

* Note: Orphan tests, that do not match any configured `markers`, will be written into all defined outputs.
 Be aware these tests do not have any references.


## Creating lobster files

Make sure to provide the YAML configuration file using `--config`.
This configuration file must also contain a list of input files or directories.
Here is a complete command:

```sh
$ lobster-cpptest --config cpptest-config.yaml
```

## Example

The LOBSTER unit tests contains a working example:

* Test [test_case.cpp](../test-unit/lobster-cpptest/data/test_case.cpp) containing requirement tags

## Notes & Caveats
* This tool supports these `markers`: '@requirement'
* This tool supports these `kind`: 'req', 'imp' and 'act'
* YAML configuration format is now required instead of the previous JSON-like .config format

## Known Issues

- The tool considers commented test cases as valid test cases and they are included in the lobster report.

  Example:
  
  Commented test case in cpp test file
  ```cpp
  /* 
  @requirement
  TEST(LayoutTest1, SingleComment){}
  */
  ```

- If list of cpp test files are provided then the tool ignores the extensions of files.
- Also, if the input files with invalid file extensions contain valid cpp tests
then the tool considers all the test cases from these files and are included in the lobster report.
