LOBSTER_ROOT := ../../..
export PYTHONPATH := $(LOBSTER_ROOT)
export PATH     := $(LOBSTER_ROOT):$(PATH)

LOBSTER_REPORT := ../basic/report.reference_output.lobster
TRACING_DIR    := traceability
SPHINX_BUILD   := sphinx-build

.PHONY: html clean

# Generate the multi-page RST report, then build Sphinx HTML.
html: $(TRACING_DIR)/index.rst
	$(SPHINX_BUILD) -b html . _build/html
	@echo ""
	@echo "HTML report written to _build/html/index.html"

$(TRACING_DIR)/index.rst: $(LOBSTER_REPORT)
	python $(LOBSTER_ROOT)/lobster-rst-report.py $< --out-dir=$(TRACING_DIR)

clean:
	rm -rf _build/ $(TRACING_DIR)/ traceability.rst
