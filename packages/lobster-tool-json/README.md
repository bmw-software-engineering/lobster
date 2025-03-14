# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from JSON files. The
tool expects a json file with a list of objects, for which you can
specify members to extract by name. It is extremely simplistic but it
may be good enough to support some use-cases.

If you have a more complex file format you will likely need to provide
your own tool for your own files.

## Tools

* `lobster-json`: Extract activities from JSON files

## Configuration via YAML

The tool uses a YAML configuration file to define the following common parameters:

  1) inputs: A list of input file paths (can include directories).
  2) out: The name of the output file where results will be stored.
  3) inputs-from-file: A file containing paths to input files or directories.
  4) single: A flag to avoid the use of multiprocessing. If true, multiprocessing will be skipped.

  * YAML Configuration Example:

    Below is an example of how you can define these parameters in the YAML configuration file:

    ```yaml
    out: "output.lobster"  # Output file where results will be written
    inputs:
        - "file1.json"
        - "file2.json"
        - "directory1/"
    inputs-from-file: "directory1/"  # File containing a list of input files or directories
    single: false  # Set to true to avoid multiprocessing
    ```

  * Command-Line Usage:

    To run the tool with the specified YAML configuration file, use the following command:

    ```bash
    lobster-json --config /path/to/config.yaml
    ```

    Where /path/to/config.yaml is the path to your YAML configuration file.

## Usage

Some projects store their test vectors in JSON files. This tool can be
used to expose these to LOBSTER. Consider this example:

```json
[
    {"name"        : "XOR Test 1",
     "values"      : [false, false],
     "expectation" : false,
     "tags"        : "example.req_xor"},

    {"name"        : "XOR Test 2",
     "values"      : [false, true],
     "expectation" : true,
     "tags"        : "example.req_xor"},

    {"name"          : "Potato Test 1",
     "values"        : [false, false],
     "expectation"   : true,
     "tags"          : null,
     "justification" : "Unlinked on purpose"}
]
```

Here we have a list of three tests. You can configure the
`lobster-json` tool to extract the relevant information:

```bash
$ lobster-json --name-attribute "name" \
               --tag-attribute "tags" \
               --justification-attribute "justification" \
               --config "/path/to/config.yaml"
```

The name attribute is optional. If your test files do not contain
names for the tests then a name is synthesised using the filename and
the index of the test (e.g. foo_1, foo_2, foo_3, etc.).

The justification attribute is also optional.

The tag attribute is not, and it needs to be present in each test
object.

The specification of these attributes can be nested, for example if
your test objects instead look like this:

```json
[
    {"meta" : {"name" : "XOR Test 1",
               "asil" : "B",
               "req"  : "example.req_xor"},
     "test" : {"inputs" : [false, false],
               "expect" : false}
    },

    ...
```

Then you can get to the data like so:

```bash
$ lobster-json --name-attribute "meta.name" \
               --tag-attribute "meta.req" \
               --justification-attribute "meta.just" \
               --config "/path/to/config.yaml"
```

Finally, if your list of tests is nested more deeply in an object, you
can use the `--test-list` flag to identify where it is. For example:

```json
{ "kind"    : "tests",
  "vectors" : [
    {"meta" : {"name" : "XOR Test 1",
               "asil" : "B",
               "req"  : "example.req_xor"},
     "test" : {"inputs" : [false, false],
               "expect" : false}
    },

    ...
```

Then you can use `--test-list=vectors` to identify the correct list.

Note: This tool is pretty limited. For the obvious cases it works
pretty well, but if you have a more complex test definition in JSON
then you will need to write your own adaptor [using the documented
schema](https://github.com/bmw-software-engineering/lobster/blob/main/documentation/schemas.md).

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
