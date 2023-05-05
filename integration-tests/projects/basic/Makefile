LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

CLANG_TIDY:=$(LOBSTER_ROOT)/../llvm-project/build/bin/clang-tidy

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

html_report.html: cppcode.lobster gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster json.lobster
	@lobster-report
	@lobster-online-report
	@cp report.lobster report.reference_output
	@lobster-html-report
	@lobster-ci-report | tee ci_report.reference_output

cppcode.lobster: foo.h foo.cpp
	@lobster-cpp foo.cpp foo.h \
		--out="cppcode.lobster" --clang-tidy $(CLANG_TIDY)

gtests.lobster: foo.h foo.cpp test.cpp
	@bazel test foo_test --cxxopt='-std=c++14'
	@lobster-gtest $(LOBSTER_ROOT)/bazel-out/*/testlogs/$(THIS_TEST) \
		--out="gtests.lobster"
	sed -i s/$(THIS_TEST_ESCAPED)\\///g gtests.lobster

mcode.lobster: nand.m nand_test.m
	@mh_trace *.m \
		--out-imp="mcode.lobster" \
		--out-act="mtests.lobster"

pycode.lobster: nor.py
	@lobster-python *.py \
		--out="pycode.lobster" \
		--parse-decorator trlc_reference requirement

software-requirements.lobster: potato.rsl potato.check potato.trlc
	@$(LOBSTER_WIP)/lobster_trlc *.rsl *.check *.trlc \
		--out="software-requirements.lobster" \
		--cb-tags="trace_cb"

json.lobster: example.json
	@lobster-json example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--out="json.lobster"
