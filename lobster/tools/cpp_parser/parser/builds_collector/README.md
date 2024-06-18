# Builds_collector

builds_collector is a library used the requirements_coverage_tool to get the status of the last ZuulBuilds for the configured pipeline.

# Usage

You need to provide the zuul credentials for the builds_collector via environment variables. Prior to running the builds_collector, verify that the following env variables are defined:
```bash
ZUUL_USERNAME
ZUUL_PASSWORD
```

# Testing

Tests are fully bazelized and can be run only with python 3.8.

You can reliably run the tests in parallel with `--jobs=N` for `N>1`, or with `--runs_per_test=M` for `M>1`, but not both at the same time. This is because some of the tests get their own fixed, unique port/socket assigned and ports/sockets cannot be used in parallel.

```
$ bazel test --//:use_python_38 //ci_config/scripts/requirements_coverage_tool/core/common/builds_collector/...
```

To learn how to test the deployment, please refer to [Contribute.md](Contribute.md).
