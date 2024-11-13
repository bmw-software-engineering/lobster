TOOL=../../lobster-json

INPUT_FILES=$(shell find . -maxdepth 2 -type f -name '*.input')
TARGETS=$(INPUT_FILES:.input=.output)

all: $(TARGETS)

%.output: %.input
	@tail -n +2 $< > $*.json
	@touch $*.lobster
	-@coverage run -p --rcfile=../../coverage.cfg --branch \
		--data-file ../../.coverage \
		$(TOOL) $(shell head -1 $< | tail --bytes=+3) --out=$*.lobster --single > $@ 2>&1
	@echo "==========" >> $@
	@cat $*.lobster >> $@
	@rm $*.json $*.lobster
