# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C++
test code. The tracing tags are identified by searching for configurable 
markers in the comments above the test code.

## Tools

This LOBSTER package contains only one tool, `lobster-cpptest`.
It can be used to extract references from C++ tests.
The most frequent use case is that, the references point to requirements.
But `lobstser-cpptest` is agnostic to that, and the references can point to any kind
of artefact.
The references must be given inside a comment above the test case itself.

The resulting `*.lobster` file will then contain a LOBSTER item per test case.
This file can be used to generate a LOBSTER report.

## Configuration

The tool requires a YAML configuration file to define its settings.
You must provide this file when running the tool to specify parameters to process.

## Usage

This tool supports C++ code.
For this your C++ tests must have a documentation with `markers`:
They can either be `@requirement`, `@requiredby` or `@defect`.
Here is an example:
```cpp
/**
 * @requirement CB-#1111, CB-#2222,
 *              CB-#3333
 * @requirement CB-#4444 CB-#5555
 *              CB-#6666
 */
TEST(RequirementTagTest1, RequirementsAsMultipleComments) {
  // your test implementation here
}
```
You can also provide parameters to specify which markers should be extracted from which files.
Additionally, you need to provide the Codebeamer URL.

Examples:

```yaml
output:
    component_tests.lobster:
        markers:
        - "@requirement"
        kind: "req"

    unit_tests.lobster:
        markers:
        - "@requiredby"
        kind: "req"

    other_tests.lobster:
        markers: []
        kind: ""

codebeamer_url: "https://codebeamer.com"
 ```
You can also include CPP files in the YAML configuration file.

```yaml
  files:
    - 'path/to/source1.cpp'
    - 'path/to/source2.cpp'
```
Note: File paths are accepted only in single quotes.

## Technical Aspects

`lobster-cpptest` now displays a test-name instead of a fixture-name 
in the lobster-report and lobster-html-report.

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
