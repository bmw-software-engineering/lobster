LOBSTER_ROOT:=../../..

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))
REFERENCE_OUTPUT:=report.reference_output

html_report.html: softreq.lobster sysreq.lobster lobster.conf
	@lobster-report
	@if diff report.lobster $(REFERENCE_OUTPUT); then \
	    echo "Files are identical"; \
    else \
        echo "Files are different"; \
        exit 1; \
	fi

softreq.lobster:
	@lobster-trlc --config="soft_req_trlc_config.yaml" \
		--out="softreq.lobster"

sysreq.lobster:
	@lobster-trlc --config="sys_req_trlc_config.yaml" \
		--out="sysreq.lobster"
