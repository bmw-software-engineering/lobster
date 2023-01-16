html_report.html: gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster
	@../../../lobster_report
	@../../../lobster_html_report report.lobster

gtests.lobster: foo.h foo.cpp test.cpp
	@bazel test foo_test
	@../../../lobster_gtest . --out="gtests.lobster"

mcode.lobster: nand.m nand_test.m
	@../../../lobster_matlab *.m \
		--code-out="mcode.lobster" \
		--test-out="mtests.lobster"

pycode.lobster: nor.py
	@../../../lobster_python *.py \
		--out="pycode.lobster"

software-requirements.lobster: potato.rsl potato.check potato.trlc
	@../../../lobster_trlc *.rsl *.check *.trlc \
		--out="software-requirements.lobster"
