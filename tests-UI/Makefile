# Makefile

# Tool paths
LOBSTER_PYTHON_TOOL := ../lobster-python
LOBSTER_REPORT_TOOL := ../lobster-report
LOBSTER_HTML_REPORT_TOOL := ../lobster-html-report

# Python script and configuration file
PYTHON_SCRIPT := ../lobster/tools/python/python.py
LOBSTER_CONFIG := lobster.config

# Output files
PYTHON_OUTPUT := python.lobster
REPORT_OUTPUT := report.lobster
HTML_REPORT_OUTPUT := test_html_report.html

# Default target
.PHONY: all
all: python-output report-output html-report-output selenium-tests clean

# Generate Python output
.PHONY: python-output
python-output:
	@echo "Running lobster-python script on: $(PYTHON_SCRIPT)"
	@python3 $(LOBSTER_PYTHON_TOOL) $(PYTHON_SCRIPT) --out=$(PYTHON_OUTPUT)

# Generate LOBSTER report
.PHONY: report-output
report-output:
	@echo "Generating LOBSTER report..."
	@python3 $(LOBSTER_REPORT_TOOL) --lobster-config=$(LOBSTER_CONFIG) --out=$(REPORT_OUTPUT)

# Generate HTML report
.PHONY: html-report-output
html-report-output:
	@echo "Generating HTML report..."
	@python3 $(LOBSTER_HTML_REPORT_TOOL) $(REPORT_OUTPUT) --out=$(HTML_REPORT_OUTPUT)

# Run Selenium tests
.PHONY: selenium-tests
selenium-tests:
	@echo "Running Selenium tests..."
	@for test in $(shell find -name "*.py"); do \
		echo "Running $$test..."; \
		python3 $$test || exit 1; \
	done

# Clean up generated files
.PHONY: clean
clean:
	@echo "Cleaning up generated files..."
	@rm -f $(PYTHON_OUTPUT) $(REPORT_OUTPUT) $(HTML_REPORT_OUTPUT)
