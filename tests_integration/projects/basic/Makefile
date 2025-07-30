LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

CLANG_TIDY:=$(LOBSTER_ROOT)/../llvm-project/build/bin/clang-tidy

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))
REFERENCE_OUTPUT:='report.reference_output.lobster'
REFERENCE_OUTPUT_WITH_HASH := report.reference_output_with_hash.lobster
REFERENCE_OUTPUT_CI:='ci_report.reference_output.log'
PYTHON = python3
UPDATE_GIT_HASHES_SCRIPT:='../../../tests_system/tests_utils/update_online_json_with_hashes.py'

html_report.html: cppcode.lobster gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster json.lobster
	@bash -c "lobster-report && echo '✅ lobster-report succeeded!' || { echo '❌ ERROR: lobster-report failed!'; exit 1; }"
	@bash -c "lobster-online-report && echo '✅ lobster-online-report succeeded!' || { echo '❌ ERROR: lobster-online-report failed!'; exit 1; }"
	$(PYTHON) $(UPDATE_GIT_HASHES_SCRIPT) $(REFERENCE_OUTPUT) $(REFERENCE_OUTPUT_WITH_HASH)
	@if diff report.lobster $(REFERENCE_OUTPUT_WITH_HASH); then echo '✅ Files are identical!'; else { echo '❌ ERROR: Files are different!'; exit 1; }; fi
	rm $(REFERENCE_OUTPUT_WITH_HASH)
	@bash -c "lobster-html-report && echo '✅ lobster-html-report succeeded!' || { echo '❌ ERROR: lobster-html-report failed!'; exit 1; }"
	@bash -c "lobster-ci-report | tee ci_report.log && echo '✅ lobster-ci-report succeeded!' || { echo '❌ ERROR: lobster-ci-report failed!'; exit 1; }"
	@if diff ci_report.log $(REFERENCE_OUTPUT_CI); then echo '✅ lobster-ci-report log file matches expectation!'; else { echo '❌ ERROR: lobster-ci-report log file does not match expectation!'; exit 1; }; fi
	rm ci_report.log

cppcode.lobster: foo.h foo.cpp
	@lobster-cpp foo.cpp foo.h \
		--out="cppcode.lobster" --clang-tidy $(CLANG_TIDY)

gtests.lobster: foo.h foo.cpp test.cpp
	@bazel test foo_test --cxxopt='-std=c++14' --enable_workspace
	@lobster-gtest $(LOBSTER_ROOT)/bazel-out/*/testlogs/$(THIS_TEST) \
		--out="gtests.lobster"
	sed -i s/$(THIS_TEST_ESCAPED)\\///g gtests.lobster

mcode.lobster: nand.m nand_test.m exclusive_or.slx
	@mh_trace *.m *.slx \
		--out-imp="mcode.lobster" \
		--out-act="mtests.lobster"

pycode.lobster: nor.py
	@lobster-python *.py \
		--out="pycode.lobster" \
		--parse-decorator trlc_reference requirement

software-requirements.lobster:
	@lobster-trlc --config="trlc_config.yaml" --out="software-requirements.lobster"

json.lobster:
	@lobster-json --config="config.yaml" \
		--out="json.lobster"
