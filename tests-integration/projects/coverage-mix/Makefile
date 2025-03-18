LOBSTER_ROOT:=../../..

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))
REFERENCE_OUTPUT:=report.reference_output

html_report.html: req_a.lobster req_b.lobster test_a.lobster lobster.conf trlc_req_a.conf trlc_req_b.conf trlc_test_spec.conf
	@lobster-report
	@if diff report.lobster $(REFERENCE_OUTPUT); then \
	    echo "Files are identical"; \
    else \
        echo "Files are different"; \
        exit 1; \
	fi

req_a.lobster: example.rsl req_a.trlc req_b.trlc test_spec.trlc
	@lobster-trlc example.rsl req_a.trlc req_b.trlc test_spec.trlc\
		--out="req_a.lobster" --config-file="trlc_req_a.conf"

req_b.lobster: example.rsl req_a.trlc req_b.trlc test_spec.trlc
	@lobster-trlc example.rsl req_a.trlc req_b.trlc test_spec.trlc\
		--out="req_b.lobster" --config-file="trlc_req_b.conf"

test_a.lobster: example.rsl req_a.trlc req_b.trlc test_spec.trlc
	@lobster-trlc example.rsl req_a.trlc req_b.trlc test_spec.trlc\
		--out="test_a.lobster" --config-file="trlc_test_spec.conf"
