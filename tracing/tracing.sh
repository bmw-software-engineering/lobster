#!/bin/bash

# Create output directories if they don't exist
mkdir -p tracing_out
mkdir -p docs

TOOLS=("codebeamer" "cpptest" "trlc" "json" "pkg" "report" "html_report")

# Process each tool
for tool in "${TOOLS[@]}"; do
    echo "Processing tool: lobster-$tool"
    TARGET_NAME="lobster_$tool"

    # Determine the correct path for the tool by checking where it exists
    if [ -d "lobster/tools/$tool" ]; then
        TOOL_PATH="$tool"
        OUTPUT_NAME="tracing-$tool.html"
    elif [ -d "lobster/tools/core/$tool" ]; then
        TOOL_PATH="core/$tool"
        OUTPUT_NAME="tracing-core_$tool.html"
    else
        echo "❌ ERROR: Tool '$tool' not found in lobster/tools/ or lobster/tools/core/"
        continue
    fi

    # Process tool in a subshell to contain errors
    if (
        set -e  # Exit subshell on error, but don't exit main script

        # Generate use cases
        python util/tracing/usecases.py \
            --target="$TARGET_NAME" \
            lobster/requirements.rsl \
            lobster/use_cases.trlc \
            "lobster/tools/$TOOL_PATH/requirements/potential_errors.trlc" \
            "lobster/tools/$TOOL_PATH/requirements/test_specifications.trlc" \
            --out=tracing_out/use-cases.lobster

        # Generate artifacts
        for artifact in potential-errors test-specifications system-requirements software-requirements; do
            python lobster-trlc.py \
                --config="tracing/lobster_$tool/$tool.$artifact.lobster-trlc.yaml" \
                --out="tracing_out/$artifact.lobster"
        done

        python lobster-python.py "lobster/tools/$TOOL_PATH" --out=tracing_out/code.lobster
        python lobster-python.py tests_system/lobster_$tool --activity \
            --out=tracing_out/system-tests.lobster
        python lobster-python.py tests_unit/lobster_$tool --activity \
            --out=tracing_out/unit-tests.lobster

        # Generate report
        python lobster-report.py --lobster-config=tracing/tracing_policy.conf \
            --out=tracing_out/tracing.lobster

        # Generate online report
        printf "report: tracing_out/tracing.lobster\n" >> tracing_out/online_report_config.yaml
        printf "commit_id: 'main'\n" >> tracing_out/online_report_config.yaml
        printf "repo_root: ''\n" >> tracing_out/online_report_config.yaml
        printf "base_url: 'https://github.com/bmw-software-engineering/lobster'" >> tracing_out/online_report_config.yaml
        python lobster-online-report.py --config=tracing_out/online_report_config.yaml --out=tracing_out/online-report.lobster

        # Generate HTML reports
        python lobster-html-report.py tracing_out/online-report.lobster \
            --out=docs/$OUTPUT_NAME
    ); then
        echo -e "✅ SUCCESS: Generated HTML report for $tool in docs/$OUTPUT_NAME"
        rm -f tracing_out/*.lobster tracing_out/*.yaml
    else
        echo -e "❌ ERROR: Failed to process $tool."
        rm -f tracing_out/*.lobster tracing_out/*.yaml
    fi

    echo "----------------------------------------"
done

echo "Tracing script completed"

# Final cleanup - remove the entire tracing_out directory
echo "Cleaning up intermediate files..."
rm -rf tracing_out
