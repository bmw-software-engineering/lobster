#!/bin/bash

# Cleanup function that runs on exit
cleanup() {
    echo "Cleaning up intermediate files..."
    rm -rf tracing-out
}

# Set trap to run cleanup on exit (normal or error)
trap cleanup EXIT

# Create output directories if they don't exist
mkdir -p tracing-out
mkdir -p docs

TOOLS=("codebeamer" "cpptest" "trlc")

# Process each tool
for tool in "${TOOLS[@]}"; do
    echo "Processing lobster-$tool..."
    
    # Process tool in a subshell to contain errors
    if (
        set -e  # Exit subshell on error, but don't exit main script
        
        # Generate use cases
        python util/tracing/usecases.py \
            --target=lobster_$tool \
            lobster/requirements.rsl \
            lobster/use_cases.trlc \
            lobster/tools/$tool/requirements/potential_errors.trlc \
            lobster/tools/$tool/requirements/test_specifications.trlc \
            --out=tracing-out/use-cases.lobster
        
        # Generate artifacts
        lobster-trlc \
            --config=tracing/lobster_$tool/$tool.potential-errors.lobster-trlc.yaml \
            --out=tracing-out/potential-errors.lobster
        lobster-trlc \
            --config=tracing/lobster_$tool/$tool.test-specifications.lobster-trlc.yaml \
            --out=tracing-out/test-specifications.lobster
        lobster-trlc \
            --config=tracing/lobster_$tool/$tool.system-requirements.lobster-trlc.yaml \
            --out=tracing-out/system-requirements.lobster
        lobster-trlc \
            --config=tracing/lobster_$tool/$tool.software-requirements.lobster-trlc.yaml \
            --out=tracing-out/software-requirements.lobster
        lobster-python lobster/tools/$tool --out=tracing-out/code.lobster
        lobster-python tests_system/lobster_$tool --activity \
            --out=tracing-out/system-tests.lobster
        lobster-python tests_unit/lobster_$tool --activity \
            --out=tracing-out/unit-tests.lobster
        
        # Generate report
        lobster-report --lobster-config=tracing/tracing_policy.conf \
            --out=tracing-out/tracing.lobster
        
        # Generate HTML report
        lobster-html-report tracing-out/tracing.lobster \
            --out=docs/tracing-$tool.html
    ); then
        echo -e "✅ SUCCESS: Generated HTML report for $tool in docs/tracing-$tool.html"
    else
        echo -e "❌ ERROR: Failed to process $tool. Continuing with next tool..."
    fi
    
    echo "----------------------------------------"
done
