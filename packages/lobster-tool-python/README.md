# LOBSTER

The **L**ightweight **O**pen **B**MW **S**oftware **T**raceability
**E**vidence **R**eport allows you to demonstrate software traceability
and requirements coverage, which is essential for meeting standards
such as ISO 26262.

This package contains a tool extract tracing tags from Python3 source
code.

## Tools

* `lobster-python`: Extrat requirements from Python3 code

## Usage

This tool supports both Python code and PyUnit unit tests.

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

For classes you have a choice on how you trace them: you either
annotate the class itself, or each individual method. If you choose to
annotate the class itself, then you will get warnings for each method
with an annotation.

For normal code the usage is:

```bash
lobster-python FILES_OR_DIRS
```

For pyunit the usage is:

```bash
lobster-python --activity FILES_OR_DIRS
```

For pyunit the tool automatically ignore any class function that is
not explicitly a test (i.e. you don't need to manually exclude your
setup or tear down code, only individual tests will be included).

## Copyright & License information

The copyright holder of LOBSTER is the Bayerische Motoren Werke
Aktiengesellschaft (BMW AG), and LOBSTER is published under the [GNU
Affero General Public License, Version
3](https://github.com/bmw-software-engineering/lobster/blob/main/LICENSE.md).
