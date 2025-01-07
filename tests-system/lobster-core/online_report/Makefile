# Makefile

LOBSTER_PYTHON_TOOL = "../../../lobster-python"
LOBSTER_REPORT_TOOL = "../../../lobster-report"
LOBSTER_ONLINE_REPORT_TOOL = "../../../lobster-online-report"

# Set the paths to the Python script and Lobster commands
PYTHON_SCRIPT = "../../../lobster/tools/python/python.py"
LOBSTER_CONFIG = "lobster.config"

# Set the output file names
PYTHON_OUTPUT = "python.lobster"
REPORT_OUTPUT = "report.lobster"
ONLINE_REPORT_OUTPUT = "online-report.lobster"
EXPECTED_OUTPUT = 'expected-output.lobster'

# Python script to update the expected git hashes
PYTHON_FILE:='../../../tests-utils/update_online_json_with_hashes.py'

# Set the Python interpreter
PYTHON = python3

# Define the default target
run: python-output	report-output online-report-output copy-output python-script compare clean

# Execute the Python script
python-output:
	@echo "Running lobster-python script on: $(PYTHON_SCRIPT)"
	$(LOBSTER_PYTHON_TOOL) $(PYTHON_SCRIPT) --out=$(PYTHON_OUTPUT)

# Generate the LOBSTER report
report-output:
	$(LOBSTER_REPORT_TOOL) --lobster-config=$(LOBSTER_CONFIG) --out=$(REPORT_OUTPUT)

# Generate the online LOBSTER report
online-report-output:
	$(LOBSTER_ONLINE_REPORT_TOOL) $(REPORT_OUTPUT) --out=$(ONLINE_REPORT_OUTPUT)

# Copy the online report to the expected output file
copy-output:
	cp $(ONLINE_REPORT_OUTPUT) $(EXPECTED_OUTPUT)

# 'python-script' target to execute the python script to update expected git hashes
python-script:
	$(PYTHON) $(PYTHON_FILE) $(EXPECTED_OUTPUT)

# Compare target to compare the expected output with the actual output
compare:
	@if diff $(ONLINE_REPORT_OUTPUT) $(EXPECTED_OUTPUT); then \
        echo "Files are identical"; \
    else \
        echo "Files are different"; \
        exit 1; \
    fi

# Clean up the generated files
clean:
	rm -f $(PYTHON_OUTPUT) $(REPORT_OUTPUT) $(ONLINE_REPORT_OUTPUT) $(EXPECTED_OUTPUT)
