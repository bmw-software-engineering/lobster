TOOL=../../lobster-python

TARGETS=$(addsuffix .output, $(basename $(wildcard **/*.py) $(wildcard *.py)))

all: $(TARGETS)

%.output: %.py
	@touch $*.lobster
	-@coverage run -p --rcfile=../../coverage.cfg --branch \
		--data-file ../../.coverage \
		$(TOOL) $(shell head -1 $< | tail --bytes=+2) $< --out=$*.lobster --single > $@ 2>&1
	@echo "==========" >> $@
	@cat $*.lobster >> $@
	@rm $*.lobster
