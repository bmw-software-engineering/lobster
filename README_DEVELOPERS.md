# Information for LOBSTER Developers

* [Release Process](documentation/release.md)
* [System Test Coverage Report](https://bmw-software-engineering.github.io/lobster/htmlcov-system/index.html)
* [Unit Test Coverage Report](https://bmw-software-engineering.github.io/lobster/htmlcov-unit/index.html)
* [LOBSTER API Documentation](https://bmw-software-engineering.github.io/lobster/api_documentation/)
* [Coding Guideline](CODING_GUIDELINE.md)
* [Requirements Guideline](lobster/tools/REQUIREMENTS.md)
* [System Test Framework](tests_system/README.md)

## Requirements Coverage

The requirement-to-test coverage is measured using LOBSTER itself.
Each LOBSTER tool has got a report on its own.
Here are the links to the individual requirement coverage reports:

* [Requirement Coverage Report TRLC](https://bmw-software-engineering.github.io/lobster/tracing-trlc.html)
* [Requirement Coverage Report Python](https://bmw-software-engineering.github.io/lobster/tracing-python.html)
* [Requirement Coverage Report PKG](https://bmw-software-engineering.github.io/lobster/tracing-pkg.html)
* [Requirement Coverage Report Json](https://bmw-software-engineering.github.io/lobster/tracing-json.html)
* [Requirement Coverage Report Gtest](https://bmw-software-engineering.github.io/lobster/tracing-gtest.html)
* [Requirement Coverage Report Cpptest](https://bmw-software-engineering.github.io/lobster/tracing-cpptest.html)
* [Requirement Coverage Report Cpp](https://bmw-software-engineering.github.io/lobster/tracing-cpp.html)
* [Requirement Coverage Report Core CI Report](https://bmw-software-engineering.github.io/lobster/tracing-core_ci_report.html)
* [Requirement Coverage Report Core HTML Report](https://bmw-software-engineering.github.io/lobster/tracing-core_html_report.html)
* [Requirement Coverage Report Core Online Report](https://bmw-software-engineering.github.io/lobster/tracing-core_online_report.html)
* Requirement Coverage Report Core Online Report Nogit: not yet available
* [Requirement Coverage Report Core Report](https://bmw-software-engineering.github.io/lobster/tracing-core_report.html)
* [Requirement Coverage Report Codebeamer](https://bmw-software-engineering.github.io/lobster/tracing-codebeamer.html)

## Updating Bazel dependencies

First update `requirements.txt`.
This file is input to the Bazel commands below.

The command for updating Bazel dependencies is usually documented in a header comment
in the relevant `requirements_lock` file, for instance `requirements_lock_3_12.txt`.

When using a corporate Python package index, run:

```sh
bazel run --enable_workspace //:python_dependencies_3_12.run -- \
  --index-url '<your-index-url>'
```

Always update dependencies for all Python versions.
