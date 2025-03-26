# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool to extract tracing tags from Python3 source
code or Bazel files.

## Tools

* `lobster-python`: Extract requirements from Python3 code or from Bazel

## Usage

This tool supports:
- Python code
- Python PyUnit/unittest unit tests
- Bazel files

`lobster-python` was invented for Python code
and throughout this document we only refer to Python.
But the tool also works for Bazel files because they are very similar to Python code.

For either code or tests you can embedd tracing tags like this:

```python
   def potato(self):
      # lobster-trace: something.example
      return "potato"
```

You can add justifications as well:

```python
   def potato(self):
      # lobster-exclude: a very good reason is here
      return "potato"
```

For classes, you have a choice on how you trace them: you either
annotate the class itself, or each individual method. If you choose to
annotate the class itself, then you will get warnings for each method
with an annotation.

### Normal Code
For normal code the usage is:

```bash
lobster-python FILES_OR_DIRS
```

Note that `FILES_OR_DIRS` should not contain any tests.
They will be treated as regular code otherwise.

### Tests
For tests (`pyunit` or `unittest`) the usage is:

```bash
lobster-python --activity FILES_OR_DIRS
```

Here `FILES_OR_DIRS` may contain additional code (like the implementation of mock classes), but only functions with
names that stick to the following pattern will be taken into
account:
- start with `_test` or `test`,
- or end with `test`.

That means you don't need to manually exclude your
setup or tear down code, only individual tests will be included.

Please note that the generated output json files always use `PyTest` as framework indicator, even if `unittest` is used:
```json
{
  "framework": "PyUnit",
  "kind": "Test"
}
```

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
