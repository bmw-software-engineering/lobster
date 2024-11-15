# Makefile for lobster-trlc project

# Directory structure
RBT_DIRS := $(wildcard rbt-*)
TEST_DIRS := $(foreach rbt_dir,$(RBT_DIRS),$(wildcard $(rbt_dir)/*/))
INPUT_DIRS := $(foreach test_dir,$(TEST_DIRS),$(test_dir)input/)
EXPECTED_DIRS := $(foreach test_dir,$(TEST_DIRS),$(test_dir)expected_output/)
ACTUAL_DIRS := $(foreach test_dir,$(TEST_DIRS),$(test_dir)actual_output/)

# Executable
TOOL=../../lobster-trlc

# Targets
.PHONY: all clean $(RBT_DIRS)

all: $(RBT_DIRS)

clean:
	rm -rf $(ACTUAL_DIRS)

$(RBT_DIRS):
	@echo "Running tests for $@..."
	@mkdir -p $(@D)/rbt-output-file/default-scenario/actual-output
	@echo "Current working directory: $(shell pwd)"
	@python $(TOOL) $(shell head -n 1 $(@D)/rbt-output-file/default-scenario/input/args.txt) > $(@D)/rbt-output-file/default-scenario/actual-output/cmd.output
	@echo "cheking tests for : $(shell pwd)"
	@if git diff --no-index rbt-output-file/default-scenario/expected-output/*.output rbt-output-file/default-scenario/actual-output/cmd.output; then \
		echo "Test case passed for $@"; \
	else \
		echo "Test case failed for $@"; \
		exit 1; \
	fi

# Also compare .lobster file