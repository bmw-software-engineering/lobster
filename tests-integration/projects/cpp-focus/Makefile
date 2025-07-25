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
UPDATE_GIT_HASHES_SCRIPT:='../../../tests-system/tests_utils/update_online_json_with_hashes.py'

html_report.html: cppcode.lobster gtests.lobster software-requirements.lobster lobster.conf
	@bash -c "lobster-report && echo '$(THIS_TEST) ✅ lobster-report succeeded!' || { echo '$(THIS_TEST) ❌ ERROR: lobster-report failed!'; exit 1; }"
	@bash -c "lobster-online-report && echo '$(THIS_TEST) ✅ lobster-online-report succeeded!' || { echo '$(THIS_TEST) ❌ ERROR: lobster-online-report failed!'; exit 1; }"
	$(PYTHON) $(UPDATE_GIT_HASHES_SCRIPT) $(REFERENCE_OUTPUT) $(REFERENCE_OUTPUT_WITH_HASH)
	@if diff report.lobster $(REFERENCE_OUTPUT_WITH_HASH); then echo '✅ Files are identical!'; else { echo '❌ ERROR: Files are different!'; exit 1; }; fi
	rm $(REFERENCE_OUTPUT_WITH_HASH)
	@bash -c "lobster-html-report && echo '$(THIS_TEST) ✅ lobster-html-report succeeded!' || { echo '$(THIS_TEST) ❌ ERROR: lobster-html-report failed!'; exit 1; }"
	@bash -c "lobster-ci-report | tee ci_report.log && echo '✅ lobster-ci-report succeeded!' || { echo '❌ ERROR: lobster-ci-report failed!'; exit 1; }"
	@if diff ci_report.log $(REFERENCE_OUTPUT_CI); then echo '✅ lobster-ci-report log file matches expectation!'; else { echo '❌ ERROR: lobster-ci-report log file does not match expectation!'; exit 1; }; fi
	rm ci_report.log

cppcode.lobster: fruit.h fruit.cpp
	@lobster-cpp fruit.cpp fruit.h \
		--out="cppcode.lobster" --clang-tidy $(CLANG_TIDY) --skip-clang-errors clang-diagnostic-error Wunused-value

gtests.lobster: fruit.h fruit.cpp fruit_test.cpp
	@bazel test //$(THIS_TEST):fruit_test --cxxopt='-std=c++14' --enable_workspace
	@lobster-gtest $(LOBSTER_ROOT)/bazel-out/*/testlogs/$(THIS_TEST)/fruit_test \
		--out="gtests.lobster"
	sed -i s/$(THIS_TEST_ESCAPED)\\///g gtests.lobster

software-requirements.lobster:
	@lobster-trlc --config="trlc_config.yaml" --out="software-requirements.lobster"
