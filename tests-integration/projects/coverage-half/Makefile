LOBSTER_ROOT:=../../..

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

html_report.html: softreq.lobster sysreq.lobster lobster.conf trlc-softreq.conf trlc-sysreq.conf
	@lobster-report
	@lobster-online-report
	@cp report.lobster report.reference_output
	@lobster-html-report

softreq.lobster: example.rsl softreq_example.trlc sysreq_example.trlc
	@lobster-trlc example.rsl softreq_example.trlc sysreq_example.trlc\
		--out="softreq.lobster" --config-file="trlc-softreq.conf"

sysreq.lobster: example.rsl softreq_example.trlc sysreq_example.trlc
	@lobster-trlc example.rsl softreq_example.trlc sysreq_example.trlc\
		--out="sysreq.lobster" --config-file="trlc-sysreq.conf"
