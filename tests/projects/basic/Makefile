CLANG_TIDY:=../../../../llvm-project/build/bin/clang-tidy

html_report.html: cppcode.lobster gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster json.lobster
	@../../../lobster_report
	@../../../lobster_online_report
	@../../../lobster_html_report
	@../../../lobster_ci_report | tee ci_report

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
		--out="pycode.lobster" \
		--parse-decorator trlc_reference requirement

software-requirements.lobster: potato.rsl potato.check potato.trlc
	@../../../lobster_trlc *.rsl *.check *.trlc \
		--out="software-requirements.lobster" \
		--cb-tags="trace_cb"

json.lobster: example.json
	@../../../lobster_json example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--out="json.lobster"
