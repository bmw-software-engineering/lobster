#!/bin/bash

# This script produces coverage report on builds_collector by combining:
# 1. A call to `pycoverage` (//bazel/tools/pycoverage/README.md), which measures
#    and reports coverage by analyzing all buuilds_collector tests.
# 2. A call to `find_and_copy_pycoverage_xmls.sh` (bazel/tools/pycoverage/find_and_copy_pycoverage_xmls.sh),
#    which finds all the reports generated in the above-mentioned call and copies them in a single folder.
# 3. A call to `pycoverage/merger` (//bazel/tools/pycoverage/merger/README.md), which merges all generated
#    `pycoverage` reports into a single `.xml` file.
#
# It should be noted, that `pycoverage` does not manage to successfully analyze certain tests, e.g. the ones
# that use testing tools other than `unittest`. For this reason:
# - Build errors may be encountered during the execution of step "1.", but they will be ignored and the
#   execution will continue.
# - Coverage reports derived from analyzing these tests will have an inaccurately low coverage measurement.
#
# This script is to be used in the following way:
#     ./check_builds_collector_coverage.sh /desired/output/directory

if [ $# -eq 0 ]
  then
    echo "Please provide the directory name where the output is to be generated!"
    exit 1
fi

OUTPUT_DIR="$1"

builds_collector_bin_dir="$(bazel info bazel-bin)/ci_config/scripts/requirements_coverage_tool/core/common/builds_collector"
generated_xmls_path="${OUTPUT_DIR}/builds_collector_pycoverage_xmls"
merged_xml_path="${OUTPUT_DIR}/builds_collector_pycoverage_merged_xml"

echo "Running pycoverage on all builds_collector tests"
bazel build --config=pycoverage --config=platform_ros --config=adp_gcc9 --keep_going -- //ci_config/scripts/requirements_coverage_tool/core/common/builds_collector/...

echo "Copying pycoverage.xml-s to ${generated_xmls_path}/"
$(bazel info workspace)/bazel/tools/pycoverage/find_and_copy_pycoverage_xmls.sh ${builds_collector_bin_dir} ${generated_xmls_path}

echo "Merging pycoverage reports from ${generated_xmls_path}/"
bazel run //bazel/tools/pycoverage/merger -- --report_dir ${generated_xmls_path} --output_dir ${merged_xml_path}

echo "Pycoverage report on builds_collector has been generated in ${merged_xml_path}/"