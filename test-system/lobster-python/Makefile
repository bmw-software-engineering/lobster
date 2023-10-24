TOOL=../../lobster-python

TARGETS=$(addsuffix .output, $(basename $(wildcard *.py)))

all: $(TARGETS)

%.output: %.py
	@touch $*.lobster
	-$(TOOL) $(shell head -1 $< | tail --bytes=+2) $< --out=$*.lobster --single > $@ 2>&1
	@echo "==========" >> $@
	@cat $*.lobster >> $@
	@rm $*.lobster
