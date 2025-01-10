LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

CLANG_TIDY:=$(LOBSTER_ROOT)/../llvm-project/build/bin/clang-tidy

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

REFERENCE_OUTPUT:='report.reference_output'
PYTHON = python3
UPDATE_GIT_HASHES_SCRIPT:='../../../tests-system/tests_utils/update_online_json_with_hashes.py'

# Python script to delete the git hashes from reference_output file
DELETE_COMMIT_IDS_PYTHON_SCRIPT:='../../../tests-system/tests_utils/delete_commit_ids_integration_test.py'

html_report.html: cppcode.lobster requirements.lobster lobster.conf json.lobster
	@lobster-report
	@lobster-online-report
	$(PYTHON) $(UPDATE_GIT_HASHES_SCRIPT) $(REFERENCE_OUTPUT)
	@if diff report.lobster $(REFERENCE_OUTPUT); then \
        echo "Files are identical"; \
    else \
        echo "Files are different"; \
        exit 1; \
    fi
	@lobster-html-report

cppcode.lobster: foo.h foo.cpp
	@lobster-cpp foo.cpp foo.h \
		--out="cppcode.lobster" --clang-tidy $(CLANG_TIDY)

requirements.lobster: example.rsl softreq_example.trlc sysreq_example.trlc
	@lobster-trlc example.rsl softreq_example.trlc sysreq_example.trlc\
		--out="requirements.lobster"

json.lobster: test_example.json
	@lobster-json test_example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--justification-attribute "justification" \
		--out="json.lobster"
