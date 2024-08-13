import json
from typing import List

import pandas as pd

from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.datatypes import ContextType
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.domain_model.test_status import (
    TestStatus,
)
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.event_logger import logging
from ci_config.scripts.requirements_coverage_tool.core.common.builds_collector.utils.zuul_utils import ZuulBuild


def collect_jsons_to_narrow_df(builds: List[ZuulBuild], context: ContextType) -> pd.DataFrame:
    """Creates dataframe from json.
    For each build, every test with its duration, status and error log
    is appended as a row in the dataframe.
    On errors or edge cases, a global problem line is appended.
    Parameters
    ----------
    builds: List[ZuulBuild]
        The builds for which the test logs should be downloaded.
    context: ContextType
        Context dictionary containing metadata of the process.
    Returns
    -------
    df_narrow: pd.DataFrame
        The created dataframe with build info.
    """
    test_names = []
    uuids = []
    statuses = []
    durations = []
    error_logs: List = []
    for build in builds:
        if build.cached:
            continue
        json_path = context["data_collection_pipeline_status"].builds[build.uuid].json_path

        if not json_path or not json_path.is_file():
            logging.debug(f"json path '{json_path}' not (yet) found")
            test_names.append("<no build result>")
            statuses.append(TestStatus.GLOBAL_PROBLEM)
            uuids.append(build.uuid)
            durations.append(-1)
            error_logs.append(None)
            continue

        with open(json_path, "r") as json_file:
            status_by_test = json.load(json_file)

        if not status_by_test.values():
            logging.warning(
                f"'{json_path}' is empty. This is probably an edge case where the CI managed to create the test output but didn't execute any test because of a global problem"
            )
            test_names.append("<no build result>")
            statuses.append(TestStatus.GLOBAL_PROBLEM)
            uuids.append(build.uuid)
            durations.append(-1)
            error_logs.append(None)
            continue

        test_names.extend(status_by_test.keys())
        uuids.extend(build.uuid for _ in status_by_test.keys())
        statuses.extend(
            TestStatus.from_string_label(s["status"])
            if "status" in s.keys()
            else TestStatus.FAILED  # build got terminated before writing test result
            for s in status_by_test.values()
        )
        durations.extend(
            s["duration"] if "status" in s.keys() else 0 for s in status_by_test.values()  # cant deduct status
        )
        error_logs.extend(s["error_log"] if "error_log" in s.keys() else None for s in status_by_test.values())
    return pd.DataFrame(
        {
            "uuid": uuids,
            "test_name": test_names,
            "test_status": statuses,
            "test_duration": durations,
            "error_log": error_logs,
        }
    )
