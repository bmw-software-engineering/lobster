html_report.html: mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster
	@../../../lobster_report
	@../../../lobster_html_report report.lobster

mcode.lobster: nand.m nand_test.m
	@../../../lobster_matlab *.m \
		--code-out="mcode.lobster" \
		--test-out="mtests.lobster"

pycode.lobster: nor.py
	@../../../lobster_python *.py \
		--out="pycode.lobster"

software-requirements.lobster: potato.rsl potato.check potato.trlc
	@../../../lobster_trlc *.rsl *.check *.trlc \
		--out="software-requirements.lobster" \
		--cb-tags="trace_cb"
