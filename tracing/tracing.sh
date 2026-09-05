#!/bin/bash

set -Eeuo pipefail

export PYTHONPATH="${PYTHONPATH:-.}:$PWD"

CURRENT_TOOL="setup"
CURRENT_PHASE="create output directories"

trap 'printf "❌ ERROR: tool %s failed during phase: %s\n" "$CURRENT_TOOL" "$CURRENT_PHASE" >&2' ERR

mkdir -p tracing_out docs

TOOLS=("codebeamer" "cpptest" "trlc" "json" "pkg" "report" "html_report" "online_report")

for tool in "${TOOLS[@]}"; do
    # delete all top-level files in tracing_out, but keep nested files
    find tracing_out -maxdepth 1 -type f -delete

    CURRENT_TOOL="$tool"
    CURRENT_PHASE="resolve tool path"
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
        printf "ERROR: tool %s failed during phase: %s (not found in lobster/tools/ or lobster/tools/core/)\n" \
            "$tool" "$CURRENT_PHASE" >&2
        exit 1
    fi

    CURRENT_PHASE="generate list of relevant use cases"
    python util/tracing/usecases.py \
        --target="$TARGET_NAME" \
        lobster/requirements.rsl \
        lobster/use_cases.trlc \
        "lobster/tools/$TOOL_PATH/requirements/potential_errors.trlc" \
        "lobster/tools/$TOOL_PATH/requirements/test_specifications.trlc" \
        --out="tracing_out/use-cases.lobster"

    for artifact in potential-errors test-specifications system-requirements software-requirements; do
        CURRENT_PHASE="generate $artifact artifact"
        python lobster-trlc.py \
            --config="tracing/lobster_$tool/$tool.$artifact.lobster-trlc.yaml" \
            --out="tracing_out/$artifact.lobster"
    done

    CURRENT_PHASE="generate implementation traces"
    python lobster-python.py "lobster/tools/$TOOL_PATH" --out="tracing_out/code.lobster"
    CURRENT_PHASE="generate system test traces"
    python lobster-python.py "tests_system/lobster_$tool" --activity \
        --out="tracing_out/system-tests.lobster"
    CURRENT_PHASE="generate unit test traces"
    python lobster-python.py "tests_unit/lobster_$tool" --activity \
        --out="tracing_out/unit-tests.lobster"

    CURRENT_PHASE="generate report"
    python lobster-report.py --lobster-config=tracing/tracing_policy.conf \
        --out="tracing_out/tracing.lobster"

    CURRENT_PHASE="create online report configuration"
    # obtain repository remote URL
    BASE_URL="$(git remote get-url origin)"
    case "$BASE_URL" in
        git@github.com:*) BASE_URL="https://github.com/${BASE_URL#git@github.com:}" ;;
        ssh://git@github.com/*) BASE_URL="https://github.com/${BASE_URL#ssh://git@github.com/}" ;;
    esac
    # remove .git suffix
    BASE_URL="${BASE_URL%.git}"
    printf "report: tracing_out/tracing.lobster\n" > "tracing_out/online_report_config.yaml"
    printf "commit_id: 'main'\n" >> "tracing_out/online_report_config.yaml"
    printf "repo_root: ''\n" >> "tracing_out/online_report_config.yaml"
    printf "base_url: '%s'\n" "$BASE_URL" >> "tracing_out/online_report_config.yaml"

    CURRENT_PHASE="generate online report"
    python lobster-online-report.py \
        --config="tracing_out/online_report_config.yaml" \
        --out="tracing_out/online-report.lobster"

    CURRENT_PHASE="generate HTML report"
    python lobster-html-report.py "tracing_out/online-report.lobster" \
        --out="tracing_out/$OUTPUT_NAME"

    CURRENT_PHASE="copy reports to docs"
    cp "tracing_out/$OUTPUT_NAME" "docs/$OUTPUT_NAME"
    EVIDENCE_LOBSTER="${OUTPUT_NAME%.html}.lobster"
    cp "tracing_out/online-report.lobster" "docs/$EVIDENCE_LOBSTER"

    CURRENT_PHASE="move generated files to tool-specific folder"
    TOOL_OUTPUT_DIR="tracing_out/$tool"
    rm -rf "$TOOL_OUTPUT_DIR"
    mkdir -p "$TOOL_OUTPUT_DIR"
    mv tracing_out/*.lobster "tracing_out/$OUTPUT_NAME" "$TOOL_OUTPUT_DIR/"


    printf "SUCCESS: generated HTML report for %s in docs/%s\n" "$tool" "$OUTPUT_NAME"

    echo "----------------------------------------"
done

echo "Tracing script completed"
