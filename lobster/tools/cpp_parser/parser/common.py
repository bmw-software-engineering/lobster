import json
import logging
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import yaml
from yaml.loader import SafeLoader

from lobster.tools.cpp_parser.parser.config import config


class TrackerMatching:
    """
    Used to match a Tracker to its analyzer and collect function
    """

    def __init__(self, coverage_analyzer, collect_function):
        self.coverage_analyzer = coverage_analyzer
        self.collect_function = collect_function


@dataclass
class BazelTarget:
    # Disabled since there are too many attributes of DataCollectionPipelineConfig
    # pylint: disable=too-many-instance-attributes
    """
    This class is used to store a Bazel build rule for one target
    """

    tags: List[str]
    srcs: List[str]
    hdrs: List[str]
    location: str
    classs: str
    files: List[str]
    flaky: bool = False
    timeout: str = ""
    gate_ci_status: str = ""
    post_ci_status: str = ""


def get_github_link(build_target: str) -> Tuple[str, str]:
    res = re.search("//(\w+)/(\w+)/", build_target)
    if res:
        repo_prefix = res.group(1)
        if repo_prefix == "application":
            repo = res.group(2)
            repo_prefix = repo
        else:
            repo = "ddad_ci_config"
        url = config.github_url + repo
        return url, repo_prefix
    else:
        raise Exception("Invalid or Incomplete build target. Please provide full build target path.")


def setup_logger(log_file, level=logging.DEBUG) -> None:
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s : %(message)s")
    logger.setLevel(level)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    if log_file:
        fileHandler = logging.FileHandler(log_file, mode="w")
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)


def build_github_base_url(base_url: str, branch: str = "master") -> str:
    return base_url + config.git_basedir + "/" + branch


def translate_to_path(src: str, workspace: str) -> Path:
    file_loc = src.replace("//", "/")
    if ":" in file_loc:
        path = workspace + file_loc.split(":")[0].strip()
        return str(Path(path) / file_loc.split(":")[1])
    else:
        return workspace + file_loc


def get_targets_for_all(workspace: str, bazel_target: str, tagged_with: str = "") -> Dict[str, BazelTarget]:
    # KHe: Not sure what the function name should mean
    # TODO: Not SP25 ready yet
    logging.info(f"Querying {bazel_target}")

    query = f"""
            bazel query \
            --noshow_progress --noshow_loading_progress --keep_going --noimplicit_deps --output=xml \
            'attr(tags, {tagged_with}, kind("_library", {bazel_target}) + kind("_test", {bazel_target}))'
            """
    query_xml = execute_path(query)
    targets = convert_xml_query(query_xml, workspace, include_headers=True)
    return targets


def get_targets_for_analysis(
    workspace: str, bazel_target: str, shall_include_filegroups: bool = False, service_pack="21"
) -> Dict[str, BazelTarget]:
    """
    Returns the list of targets of type cc_test and cc_binary required by the bazel_target

    Parameters
    ----------
    workspace: str
        Bazel workspace
    bazel_target: str
        Bazel target from which to get the targets from
    shall_include_filegroups: bool
        If set to True, returns the filegroups as part of the dictionary

    Returns
    -------
    Dict[str, BazelTarget]
        Dictionnary containing all parsed BazelTarget
        Keys of the dictionnary are the bazel builds rules
    """
    logging.info(f"Querying {bazel_target}")
    if service_pack == "25":
        bazel_query = "bazel aquery --output=text --include_commandline=false --config=ad_gen_25"
    else:
        bazel_query = (
            "bazel query --noshow_progress --noshow_loading_progress --keep_going --noimplicit_deps --output=xml"
        )

    bazel_query += f" 'kind(cc_test, ({bazel_target})) + kind(cc_binary, ({bazel_target}))"
    if shall_include_filegroups:
        bazel_query += f" + kind(filegroup, ({bazel_target}))"
    bazel_query += "'"

    if service_pack == "25":
        query_text = execute_path(bazel_query)
        targets = convert_text_query(query_text, workspace)
    else:
        query_xml = execute_path(bazel_query)
        targets = convert_xml_query(query_xml, workspace, service_pack=service_pack)
    return targets


def get_targets_for_filegroup(workspace: str, bazel_target: str) -> Dict[str, BazelTarget]:
    """
    Returns the list of targets of type filegroup required by the bazel_target

    Parameters
    ----------
    workspace: str
        Bazel workspace
    bazel_target: str
        Bazel target from which to get the targets from

    Returns
    -------
    Dict[str, BazelTarget]
        Dictionnary containing all parsed BazelTarget
    """
    # TODO: Not SP25 ready yet
    logging.info(f"Querying {bazel_target}")

    query = f"""
            bazel query \
            --noshow_progress --noshow_loading_progress --keep_going --noimplicit_deps --output=xml \
            'kind(filegroup,  ({bazel_target}))'
            """
    query_xml = execute_path(query)
    targets = convert_xml_query(query_xml, workspace)
    return targets


def get_files_for_analysis(workspace: str, bazel_target: str, service_pack="21") -> List[str]:
    """
    Returns the list of files that should be analyzed for the bazel_target

    Parameters
    ----------
    workspace: str
        Bazel workspace
    bazel_target: str
        Bazel target

    Returns
    -------
    List[str]
        List of files
    """
    targets = get_targets_for_analysis(
        workspace, bazel_target, shall_include_filegroups=True, service_pack=service_pack
    )
    logging.info(f"Parse bazel query for test files for {list(targets)}")

    files_found = [_file for _, target_rule in targets.items() for _file in target_rule.files]
    unique_files_found = []
    for el in files_found:
        if el not in unique_files_found:
            unique_files_found.append(el)

    msg = (
        f"The following files will be verified: {unique_files_found}" if unique_files_found else "No test files found."
    )
    logging.info(msg)

    return unique_files_found


def convert_xml_query(
    query_xml: str, workspace: str, include_headers: bool = False, service_pack: str = "21"
) -> Dict[str, BazelTarget]:
    """
    Convert the bazel xml query_xml (from a bazel query) into a dictionary.

    Parameters
    ----------
    query_xml: str
        Bazel XML query to translate into a dictionnary
    workspace: str
        Bazel workspace
    include_headers: bool
        If True, include the headers in the dictionnary

    Returns
    -------
    Dict[str, BazelTarget]
        Dictionnary containing all parsed BazelTarget
        Keys of the dictionnary are the bazel builds rules
    """

    if query_xml == "":
        return {}

    query_root = ET.fromstring(query_xml)
    rules = query_root.findall("rule")
    targets = {}
    for rule in rules:
        attrib_list = rule.findall("list")
        attrib_boolean = rule.findall("boolean")
        attrib_string = rule.findall("string")

        xml_list_objects = get_xml_obj(attrib_list, ["srcs", "hdrs", "tags"])
        xml_boolean_objects = get_xml_obj(attrib_boolean, ["flaky"])
        xml_string_objects = get_xml_obj(attrib_string, ["timeout"])

        tags = (
            [tag.attrib["value"] for tag in xml_list_objects["tags"].findall("string")]
            if xml_list_objects.get("tags", None) is not None
            else []
        )
        srcs = []
        if xml_list_objects.get("srcs", None) is not None:
            for src in xml_list_objects["srcs"].findall("label"):
                # If the source has no extension ending, this is a bazel alias
                if src.attrib["value"].split("/")[-1].find(".") == -1:
                    # Run bazel query again
                    local_targets_for_analysis = get_targets_for_analysis(
                        workspace=workspace,
                        bazel_target=src.attrib["value"],
                        shall_include_filegroups=True,
                        service_pack=service_pack,
                    )
                    if src.attrib["value"] in local_targets_for_analysis:
                        srcs.extend(
                            local_targets_for_analysis[src.attrib["value"]].srcs,
                        )
                elif has_file_allowed_ending(src.attrib["value"]):
                    srcs.append(src.attrib["value"])

        # Filter out wrong service pack
        srcs = service_pack_filter(srcs, service_pack)

        flaky = (
            xml_boolean_objects["flaky"].attrib["value"].capitalize()
            if xml_boolean_objects.get("flaky", None) is not None
            else "False"
        )
        hdrs = (
            [hdr.attrib["value"] for hdr in xml_list_objects["hdrs"].findall("label")]
            if xml_list_objects.get("hdrs", None) is not None
            else []
        )
        files = (
            list(map(lambda src: translate_to_path(src, workspace), srcs + hdrs))
            if include_headers
            else list(map(lambda src: translate_to_path(src, workspace), srcs))
        )
        timeout = (
            xml_string_objects["timeout"].attrib["value"] if xml_string_objects.get("timeout", None) is not None else ""
        )

        targets[rule.attrib["name"]] = BazelTarget(
            tags, srcs, hdrs, rule.attrib["location"], rule.attrib["class"], files, flaky, timeout
        )
    return targets


def convert_text_query(query_text: str, workspace: str) -> Dict[str, BazelTarget]:
    """
    Convert the bazel text query_text (from bazel aquery) into a dictionary.

    Parameters
    ----------
    query_text: str
        Bazel test query to translate into a dictionnary
    workspace: str
        Bazel workspace

    Returns
    -------
    Dict[str, BazelTarget]
        Dictionnary containing all parsed BazelTarget
        Keys of the dictionnary are the bazel builds rules
    """
    targets = {}
    if query_text == "":
        return targets

    query_dict = aquery_to_dict(query_text)
    # Extract the targets and inputs from all actions with Mnemonic in ["CppCompile", "Middleman"]
    # Build the dict of BazelTarget based on the "Target" field
    for key in query_dict:
        if query_dict[key]["Mnemonic"] in ["Middleman", "CppCompile"]:
            for _file in query_dict[key]["Inputs"]:
                if has_file_allowed_ending(_file):
                    if query_dict[key]["Target"] not in targets.keys():
                        targets[query_dict[key]["Target"]] = BazelTarget(
                            [], ["//" + _file], [], "", "", [translate_to_path("/" + _file, workspace)]
                        )
                    else:
                        targets[query_dict[key]["Target"]].srcs.append("//" + _file)
                        targets[query_dict[key]["Target"]].files.append(translate_to_path("/" + _file, workspace))

    # TODO : For now all other fields of BazelTarget are left empty, since they are not consumed anywhere else
    return targets


def aquery_to_dict(query_text: str) -> Dict:
    """
    Returns a dict of dict, where the keys are the action names, and the values are the action yamls
    """
    returned_dict = {}
    # Each el of splitted text is a yaml parsable
    splitted_text = query_text.split("\n\n")
    for mini_text in splitted_text:
        # Each el of val is a key: val
        val = mini_text.replace("  ", '"').replace(": ", '": ')
        splitted = val.split("\n")
        title = splitted[0]
        modified_text = ""
        for el in splitted[1:]:
            if el.startswith('"Execution platform":'):
                el = el.replace('"Execution platform": ', '"Execution platform": "')
                el = el + '"'
            modified_text += el + "\n"
        data = yaml.load(modified_text, Loader=SafeLoader)
        returned_dict[title] = data
    return returned_dict


def execute_path(cmd):
    execution_path = Path(__file__).resolve().parent
    my_env = os.environ
    my_env["HOME"] = os.getcwd().split("/.cache/bazel")[0]

    logging.info(f"Executing query {cmd}")
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=execution_path, env=my_env)
    stdout, _ = proc.communicate()
    return stdout.decode("utf-8").strip()


def has_file_allowed_ending(src_file_name):
    return src_file_name.endswith((".h", ".hh", "hpp", ".hxx", ".hcc", ".c", ".cc", ".cpp", ".cxx", ".py", ".json"))


def service_pack_filter(files_list, service_pack="21"):
    """
    Filter out all files that are not relevant for a specific service pack, based on file or folder naming
    """
    if service_pack not in ["21", "25"]:
        raise Exception("Unknown service pack")
    if not isinstance(files_list, list):
        files_list = [files_list]
    filtered_files_list = []
    # For now, only filters sp21 out of sp25 and vice-versa
    if service_pack == "25":
        # Filter sp21 specific files out
        for _file in files_list:
            if _file.find("sp21") == -1:
                filtered_files_list.append(_file)
    elif service_pack == "21":
        # Filter sp25 specific files out
        for _file in files_list:
            if _file.find("sp25") == -1:
                filtered_files_list.append(_file)
    return filtered_files_list


def get_xml_obj(attributes, properties):
    xml_objects = {}
    for attribute in attributes:
        for property in properties:
            if attribute.attrib["name"] == property:
                xml_objects[property] = attribute

    return xml_objects


def write_report(data: any, path: Path, fmt: str = "text"):
    """
    Write data to the given file using the specified format

    Parameters:
    data     -- Data to be written to path
    path     -- Path where to store the data.
    fmt      -- Format of the file, default: "text"
    """
    formats = {
        "text": lambda path, data: str(data),
        "json": lambda path, data: data.to_json() if isinstance(data, pd.DataFrame) else json.dumps(data),
        "excel": lambda path, data: data.to_excel(path, "Requirements")
        if isinstance(data, pd.DataFrame)
        else str(data),
        "csv": lambda path, data: data.to_csv(path, sep=";") if isinstance(data, pd.DataFrame) else str(data),
    }

    if fmt not in formats:
        logging.info(f"Format '{fmt}' not supported. Falling back to default")
        fmt = "text"

    try:
        logging.info(f"Exporting report as {fmt} to {path}")

        formatted_data = formats[fmt](path, data)

        # write formatted data to path if data has only been formatted
        # i.e. has not been written
        if type(formatted_data) == str:
            with open(path, "wt") as output_file:
                output_file.write(formatted_data)

    except Exception as e:
        logging.error(f"Failed to write report with {e}")
        raise e


def check_create_output_folder(dir):
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except PermissionError:
        logging.error("You don't seem to have the rights to access output folder")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Creating output directories failed. {type(e)}: {e}")
        sys.exit(1)
