TOOL=../../lobster-json

TARGETS=$(addsuffix .output, $(basename $(wildcard *.input)))

all: $(TARGETS)

%.output: %.input
	@tail +2 $< > $*.json
	@touch $*.lobster
	-$(TOOL) $(shell head -1 $< | tail --bytes=+3) --out=$*.lobster --single > $@ 2>&1
	@echo "==========" >> $@
	@cat $*.lobster >> $@
	@rm $*.json $*.lobster
