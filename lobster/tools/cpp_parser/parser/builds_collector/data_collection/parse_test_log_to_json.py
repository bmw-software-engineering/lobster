import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import (
    ContextType,
    LogInfo,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild

_RE_TEST_PATTERN = re.compile(
    r"""
    ^(//\S+)\s+ # Test name
    (NO[ ]STATUS|\(cached\)[ ]PASSED|PASSED|FAILED|TIMEOUT|FLAKY)# Test status
    (?:,[ ]failed)?[ ] # optional information for flaky tests only
    (?: # NO STATUS does not have this information
    (in[ ]\d+[ ]out[ ]of[ ]\d+[ ])? # Optional shots for flaky tests
    in[ ](\d+\.\d+)s # Test duration in seconds
    )?
    """,
    re.VERBOSE,
)
_RE_AVG_TIME_PATTERN = re.compile(r"avg = (\d+.\d+)s")
_RE_TAG_OPEN = re.compile(r"={20} Test output for (//\S+)(?:\s\(.*\))?:$")
_RE_TAG_CLOSE = re.compile(r"^={80}$")
FILTER = (
    "[ERROR]",
    "[ WARN]",
    "[FATAL]",
    " (",
    "[Error]",
    "[Warning]",
    "[Info]",
    "[Debug]",
)


def parse_test_log_to_json(build: ZuulBuild, context: ContextType) -> None:
    """Parses the test log for information.
    Parses the generated build test log for test information.
    After parsing, a marker given in the spec is set to enable caching.
    Parameters
    ----------
    build: ZuulBuild
        The build for which logs should be parsed.
    context: ContextType
        Context dictionary containing metadata of the process.
    """
    build_directory = context["data_collection_pipeline_config"].output_directory / build.uuid
    cached_marker_path = build_directory / "CACHED_PARSED_TO_JSON"

    parsed_json_path = build_directory / "parsed_status_by_test.json"
    cache_parsing = context["data_collection_pipeline_config"].enable_caching
    if cache_parsing and cached_marker_path.exists():
        context["data_collection_pipeline_status"].builds[build.uuid].json_path = parsed_json_path
        logging.debug(f"'{build_directory}' already parsed to json, skipping")
        return

    log_path = context["data_collection_pipeline_status"].builds[build.uuid].log_path
    if not log_path or not log_path.is_file():
        logging.warning(f"Log_path '{log_path}' not set")
        return
    log_url = context["data_collection_pipeline_status"].builds[build.uuid].log_url
    if not log_url:
        logging.debug(f"Log_url '{log_url}' not set")
        return
    status_by_test = _parse_log(log_path, log_url, context["data_collection_pipeline_config"].max_log_length)
    with open(parsed_json_path, "w") as json_file:
        json.dump(status_by_test, json_file)
    context["data_collection_pipeline_status"].builds[build.uuid].json_path = parsed_json_path
    logging.debug(f"Leaving marker '{cached_marker_path}'")
    cached_marker_path.touch()


def _parse_log(file_path: Path, log_url: str, tail: int) -> Dict[str, Dict[str, Any]]:
    """Parses the test log for information.
    Parses the generated build test log for test information.
    Tries to match a test name and extract its status and duration.
    For tests with multiple shots we take the average duration from the next line.
    The error log follows later in the file, the result gets update accordingly.
    To keep the log small irrelevant information is filtered and the log is shortened.
    Parameters
    ----------
    file_path: pathlib.Path
        The file location.
    log_url: str
        The url to the specific log file.
    tail: int
        Parameter to shorten error logs.
    Returns
    -------
    status_by_test: Dict[str, Dict[str, Any]]:
        Test information in the form
        {"test_name" : {"status": "x", "duration": "y", "error_log": LogInfo}}.
    """
    status_by_test: Dict[str, Dict[str, str]] = defaultdict(dict)
    with open(file_path, "r", encoding="utf8", errors="backslashreplace", newline="\n") as file_:
        number = 1
        for line in file_:
            maybe_match = _RE_TEST_PATTERN.search(line)
            if maybe_match:
                if maybe_match.group(4):
                    duration = float(maybe_match.group(4))
                else:
                    duration = -1
                if maybe_match.group(3):
                    line = next(file_)
                    number += 1
                    avg_match = _RE_AVG_TIME_PATTERN.search(line)
                    duration = float(avg_match.group(1))
                entry = {"status": maybe_match.group(2), "duration": duration}
                status_by_test[maybe_match.group(1)].update(entry)
            test_log_match = _RE_TAG_OPEN.search(line)
            if test_log_match:
                log_line = number
                error_message = ""
                line = next(file_)
                number += 1
                while not _RE_TAG_CLOSE.search(line):
                    if not line.startswith(FILTER):
                        error_message += line
                    line = next(file_, None)
                    if line is None:
                        return status_by_test
                    number += 1
                status_by_test[test_log_match.group(1)].update(
                    {"error_log": LogInfo(_tail_log(error_message, tail), log_url, log_line)._asdict()}
                )
            number += 1
    return status_by_test


def _tail_log(error_message: str, tail: int) -> str:
    """Returns last tail lines from the error_message.
    Parameters
    ----------
    error_message: str
        The sting to be cut.
    tail: int
        The number of lines to return.
    """
    return "\n".join(error_message.rstrip("\n").split("\n")[-tail:]) + "\n"
