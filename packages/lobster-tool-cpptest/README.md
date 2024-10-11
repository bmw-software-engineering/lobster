# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from ISO C or C++
source code. This tool is also extracting configurable markers/ test-types 
from the provided comments in cpp files

## Tools

* `lobster-cpptest`: Extract requirements with dynamic refrences 
  from comments.

## Usage

This tool supports C/C++ code.

For this you can provide some cpp file with these comments:

```cpp
/**
 * @requirement CB-#1111, CB-#2222,
 *              CB-#3333
 * @requirement CB-#4444 CB-#5555
 *              CB-#6666
 */
TEST(RequirementTagTest1, RequirementsAsMultipleComments) {}
```
You can also provide a config-file which determines which markers 
should be extracted in which files. In addition you have to provide 
the codebeamer-url:

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


## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
