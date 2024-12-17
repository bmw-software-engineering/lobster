# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code. The tracing tags are identified by searching for configurable 
markers in the comments of the source code.

## Tools

* `lobster-cpptest`: Extract requirements with dynamic refrences 
  from comments.

## Configuration

The tool requires a YAML configuration file to define its settings.
You must provide this file when running the tool to specify parameters to process.

## Usage

This tool supports C/C++ code.

For this you have to provide a C/C++ test documentation with `markers`:

`Markers` can be either `@requirement`, `@requiredby` or `@defect`.

```cpp
/**
 * @requirement CB-#1111, CB-#2222,
 *              CB-#3333
 * @requirement CB-#4444 CB-#5555
 *              CB-#6666
 */
TEST(RequirementTagTest1, RequirementsAsMultipleComments) {}
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

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
