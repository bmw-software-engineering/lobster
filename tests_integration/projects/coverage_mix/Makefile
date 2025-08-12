LOBSTER_ROOT:=../../..

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))
REFERENCE_OUTPUT:=report.reference_output

html_report.html: req_a.lobster req_b.lobster test_a.lobster lobster.conf
	@lobster-report
	@if diff report.lobster $(REFERENCE_OUTPUT); then \
	    echo "Files are identical"; \
    else \
        echo "Files are different"; \
        exit 1; \
	fi

req_a.lobster:
	@lobster-trlc --config="trlc_req_a.yaml" \
		--out="req_a.lobster"

req_b.lobster:
	@lobster-trlc --config="trlc_req_b.yaml" \
		--out="req_b.lobster"

test_a.lobster:
	@lobster-trlc --config="trlc_test_spec.yaml" \
		--out="test_a.lobster"
