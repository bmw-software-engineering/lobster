# How to Contribute to builds_collector

builds_collector is a library used the requirements_coverage_tool to get the status of the last ZuulBuilds for the configured pipeline.

# How to Unit Test builds_collector

```bash
bazel test --//:use_python_38 //ci_config/scripts/requirements_coverage_tool/core/common/builds_collector/...
```

# How to measure test coverage for builds_collector

Builds_collector coverage can be measured via `pycoverage`, as described in [README.md](https://cc-github.bmwgroup.net/swh/ddad/blob/master/bazel/tools/pycoverage/README.md), which will generate an `.xml` coverage report file for each analyzed test target.
Subsequentlly, the [find_and_copy_pycoverage_xmls.sh](https://cc-github.bmwgroup.net/swh/ddad/blob/master/bazel/tools/pycoverage/find_and_copy_pycoverage_xmls.sh) can be used to gather all the generated `pycoverage` reports into a single folder.
Finally, all the generated `pycoverage` reports can be merged into one using `pycoverage/merger`, as described in [README.md](https://cc-github.bmwgroup.net/swh/ddad/blob/master/bazel/tools/pycoverage/merger/README.md).

For the sake of convenience, a simple bash script has been created - [check_builds_collector_coverage.sh](https://cc-github.bmwgroup.net/swh/ddad/blob/master/ci_config/scripts/requirements_coverage_tool/core/common/builds_collector/check_builds_collector_coverage.sh) -, which combines the three above-mentioned steps.
The script in question is to be used in the following way:
```bash
./check_builds_collector_coverage.sh /desired/output/directory
```

