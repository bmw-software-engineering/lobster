LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

CLANG_TIDY:=$(LOBSTER_ROOT)/../llvm-project/build/bin/clang-tidy

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

html_report.html: cppcode.lobster requirements.lobster lobster.conf json.lobster
ifeq ($(CI), true)
	lobster-report --lobster-config lobster_ci.conf
else
	lobster-report
endif
	@lobster-online-report
	@cp report.lobster report.reference_output
	@lobster-html-report

cppcode.lobster: foo.h foo.cpp
ifneq ($(CI), true)
	lobster-cpp foo.cpp foo.h --out="cppcode.lobster" --clang-tidy $(CLANG_TIDY)
endif

requirements.lobster: example.rsl softreq_example.trlc sysreq_example.trlc
	@lobster-trlc example.rsl softreq_example.trlc sysreq_example.trlc\
		--out="requirements.lobster"

json.lobster: test_example.json
	@lobster-json test_example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--justification-attribute "justification" \
		--out="json.lobster"
