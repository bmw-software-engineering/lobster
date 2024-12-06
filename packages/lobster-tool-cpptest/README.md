# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code. The tracing tags are identified by searching for configurable 
markers in the comments of the source code.

## Tools

* `lobster-cpptest`: Extract requirements with specific references 
  from tests.

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
You have to provide a config-file which determines which `markers` should be extracted in which output-files.
The expected `kind` for each output-file should also be specified.  

* Note: If you want to extract the other tests with other `markers`,
 you can use an empty list as `markers` value. Be aware in this case the tests do not have any references.


```config
{
    "markers": [],
    "kind": "req"
}
```

In addition, you have to provide the codebeamer-url:

`Kind` can be either `req`, `imp` or `act`.

```config
{
	"output": {
		"unit_tests.lobster" : 
            {
                "markers": ["@requirement"],
                "kind": "req"
            },
        "components_tests.lobster" :
            {
                "markers": ["@requiredby", "@requirement"],
                "kind": "imp"
            }
	},
	"codebeamer_url": "https://codebeamer.example.com/test"
}
 ```

For more information about how to setup cpp and config files take a look at [manual-lobster_cpptest](../../documentation/manual-lobster_cpptest.md)


## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
