CLANG_TIDY:=../../../../llvm-project/build/bin/clang-tidy

html_report.html: cppcode.lobster gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster
	@../../../lobster_report
	@../../../lobster_html_report report.lobster

cppcode.lobster: foo.h foo.cpp
	@../../../lobster_cpp foo.cpp foo.h --out="cppcode.lobster" --clang-tidy $(CLANG_TIDY)

gtests.lobster: foo.h foo.cpp test.cpp
	@bazel test foo_test --cxxopt='-std=c++14'
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
