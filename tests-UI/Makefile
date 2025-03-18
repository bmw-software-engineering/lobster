# Makefile

# Tool paths
LOBSTER_HTML_REPORT_TOOL := ../lobster-html-report

# Output files
REPORT_OUTPUT := report.output
HTML_REPORT_OUTPUT := test_html_report.html

# Default target
.PHONY: all
all: html-report-output selenium-tests clean

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
	@rm -f $(HTML_REPORT_OUTPUT)
