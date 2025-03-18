#!/usr/bin/env python3
#
# lobster_codebeamer - Extract codebeamer items for LOBSTER
# Copyright (C) 2023-2025 Bayerische Motoren Werke Aktiengesellschaft (BMW AG)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

# This tool is based on the codebeamer Rest API v3, as documented here:
# https://codebeamer.com/cb/wiki/11631738
#
# There are some assumptions encoded here that are not clearly
# documented, in that items have a type and the type has a name.
#
#
# Main limitations:
# * Item descriptions are ignored right now
# * Branches (if they exist) are ignored
# * We only ever fetch the HEAD item
#
# However you _can_ import all the items referenced from another
# lobster artefact.

import os
import sys
import argparse
import netrc
from urllib.parse import quote
from enum import Enum
import requests
import yaml

from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.location import Codebeamer_Reference
from lobster.errors import Message_Handler, LOBSTER_Error
from lobster.io import lobster_read, lobster_write
from lobster.version import get_version

TOKEN = 'token'
REFERENCES = 'references'


class CodebeamerError(Exception):
    pass


class SupportedConfigKeys(Enum):
    """Helper class to define supported configuration keys."""
    IMPORT_TAGGED = "import_tagged"
    IMPORT_QUERY  = "import_query"
    VERIFY_SSL    = "verify_ssl"
    PAGE_SIZE     = "page_size"
    REFS          = "refs"
    SCHEMA        = "schema"
    CB_TOKEN      = "token"
    CB_ROOT       = "root"
    CB_USER       = "user"
    CB_PASS       = "pass"
    TIMEOUT       = "timeout"
    OUT           = "out"

    @classmethod
    def as_set(cls) -> set:
        return {parameter.value for parameter in cls}


def add_refs_references(req, flat_values_list):
    # refs
    for value in flat_values_list:
        if value.get("id"):
            ref_id = value.get("id")
            req.add_tracing_target(Tracing_Tag("req", str(ref_id)))


map_reference_name_to_function = {
    SupportedConfigKeys.REFS.value: add_refs_references
}


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


def query_cb_single(cb_config, url):
    assert isinstance(cb_config, dict)
    assert isinstance(url, str)

    try:
        if cb_config["token"]:
            auth = BearerAuth(cb_config["token"])
        else:
            auth = (cb_config["user"],
                    cb_config["pass"])

        result = requests.get(url,
                              auth=auth,
                              timeout=cb_config["timeout"],
                              verify=cb_config["verify_ssl"])
    except requests.exceptions.ReadTimeout:
        print("Timeout when fetching %s" % url)
        print("You can either:")
        print("* increase the timeout with --timeout")
        print("* decrease the query size with --query-size")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print("Could not fetch %s" % url)
        print(err)
        sys.exit(1)

    if result.status_code != 200:
        print("Could not fetch %s" % url)
        print("Status = %u" % result.status_code)
        print(result.text)
        sys.exit(1)

    return result.json()


def get_single_item(cb_config, item_id):
    assert isinstance(item_id, int) and item_id > 0

    url = "%s/items/%u" % (cb_config["base"],
                           item_id)
    data = query_cb_single(cb_config, url)
    return data


def get_many_items(cb_config, item_ids):
    assert isinstance(item_ids, set)

    rv = []

    page_id = 1
    query_string = quote(f"item.id IN "
                         f"({','.join(str(item_id) for item_id in item_ids)})")

    while True:
        base_url = "%s/items/query?page=%u&pageSize=%u&queryString=%s"\
                   % (cb_config["base"], page_id,
                      cb_config["page_size"], query_string)
        data = query_cb_single(cb_config, base_url)
        rv += data["items"]
        if len(rv) == data["total"]:
            break
        page_id += 1

    return rv


def get_query(mh, cb_config, query):
    assert isinstance(mh, Message_Handler)
    assert isinstance(cb_config, dict)
    assert isinstance(query, (int, str))
    rv = []
    url = ""
    page_id = 1
    total_items = None

    while total_items is None or len(rv) < total_items:
        print("Fetching page %u of query..." % page_id)
        if isinstance(query, int):
            url = ("%s/reports/%u/items?page=%u&pageSize=%u" %
                    (cb_config["base"],
                        query,
                        page_id,
                        cb_config["page_size"]))
        elif isinstance(query, str):
            url = ("%s/items/query?page=%u&pageSize=%u&queryString=%s" %
                    (cb_config["base"],
                        page_id,
                        cb_config["page_size"],
                        query))
        data = query_cb_single(cb_config, url)
        assert len(data) == 4

        if page_id == 1 and len(data["items"]) == 0:
            # lobster-trace: codebeamer_req.Get_Query_Zero_Items_Message
            print("This query doesn't generate items. Please check:")
            print(" * is the number actually correct?")
            print(" * do you have permissions to access it?")
            print(f"You can try to access '{url}' manually to check.")

        if page_id != data["page"]:
            raise CodebeamerError(f"Page mismatch in query result: expected page "
                                  f"{page_id} from codebeamer, but got {data['page']}")

        if page_id == 1:
            total_items = data["total"]
        elif total_items != data["total"]:
            raise CodebeamerError(f"Item count mismatch in query result: expected "
                                  f"{total_items} items so far, but page "
                                  f"{data['page']} claims to have sent {data['total']} "
                                  f"items in total.")

        if isinstance(query, int):
            rv += [to_lobster(cb_config, cb_item["item"])
                    for cb_item in data["items"]]
        elif isinstance(query, str):
            rv += [to_lobster(cb_config, cb_item)
                    for cb_item in data["items"]]

        page_id += 1

    assert total_items == len(rv)

    return rv


def get_schema_config(cb_config):
    """
    The function returns a schema map based on the schema mentioned
    in the cb_config dictionary.

    If there is no match, it raises a KeyError.

    Positional arguments:
    cb_config -- configuration dictionary containing the schema.

    Returns:
    A dictionary containing the namespace and class associated with the schema.

    Raises:
    KeyError -- if the provided schema is not supported.
    """
    schema_map = {
        'requirement': {"namespace": "req", "class": Requirement},
        'implementation': {"namespace": "imp", "class": Implementation},
        'activity': {"namespace": "act", "class": Activity},
    }
    schema = cb_config.get("schema", "requirement").lower()

    if schema not in schema_map:
        raise KeyError(f"Unsupported SCHEMA '{schema}' provided in configuration.")

    return schema_map[schema]


def to_lobster(cb_config, cb_item):
    assert isinstance(cb_config, dict)
    assert isinstance(cb_item, dict) and "id" in cb_item

    # This looks like it's business logic, maybe we should make this
    # configurable?

    categories = cb_item.get("categories")
    if categories:
        kind = categories[0].get("name", "codebeamer item")
    else:
        kind = "codebeamer item"

    status = cb_item["status"].get("name", None) if "status" in cb_item else None

    # Get item name. Sometimes items do not have one, in which case we
    # come up with one.
    if "name" in cb_item:
        item_name = cb_item["name"]
    else:
        item_name = "Unnamed item %u" % cb_item["id"]

    schema_config = get_schema_config(cb_config)

    # Construct the appropriate object based on 'kind'
    common_params = _create_common_params(
        schema_config["namespace"], cb_item,
        cb_config["root"], item_name, kind)
    item = _create_lobster_item(
        schema_config["class"],
        common_params, item_name, status)

    if cb_config.get(REFERENCES):
        for reference_name, displayed_chosen_names in (
                cb_config[REFERENCES].items()):
            if reference_name not in map_reference_name_to_function:
                continue

            for displayed_name in displayed_chosen_names:
                if cb_item.get(displayed_name):
                    flat_values_list = cb_item.get(displayed_name) if (
                        isinstance(cb_item.get(displayed_name), list)) \
                        else [cb_item.get(displayed_name)]
                else:
                    flat_values_list = [value for custom_field
                                        in cb_item["customFields"]
                                        if custom_field["name"] == displayed_name and
                                        custom_field.get("values")
                                        for value in custom_field["values"]]
                if not flat_values_list:
                    continue

                (map_reference_name_to_function[reference_name]
                 (item, flat_values_list))

    return item


def _create_common_params(namespace: str, cb_item: dict, cb_root: str,
                           item_name: str, kind: str):
    """
    Creates and returns common parameters for a Codebeamer item.
    Args:
    namespace (str): Namespace for the tag.
    cb_item (dict): Codebeamer item dictionary.
    cb_root (str): Root URL or path of Codebeamer.
    item_name (str): Name of the item.
    kind (str): Type of the item.
    Returns:
    dict: Common parameters including tag, location, and kind.
    """
    return {
        'tag': Tracing_Tag(
            namespace=namespace,
            tag=str(cb_item["id"]),
            version=cb_item["version"]
        ),
        'location': Codebeamer_Reference(
            cb_root=cb_root,
            tracker=cb_item["tracker"]["id"],
            item=cb_item["id"],
            version=cb_item["version"],
            name=item_name
        ),
        'kind': kind
    }


def _create_lobster_item(schema_class, common_params, item_name, status):
    """
    Creates and returns a Lobster item based on the schema class.
    Args:
    schema_class: Class of the schema (Requirement, Implementation, Activity).
    common_params (dict): Common parameters for the item.
    item_name (str): Name of the item.
    status (str): Status of the item.
    Returns:
    Object: An instance of the schema class with the appropriate parameters.
    """
    if schema_class is Requirement:
        return Requirement(
            **common_params,
            framework="codebeamer",
            text=None,
            status=status,
            name= item_name
        )

    elif schema_class is Implementation:
        return Implementation(
            **common_params,
            language="python",
            name= item_name,
        )

    else:
        return Activity(
            **common_params,
            framework="codebeamer",
            status=status
        )


def import_tagged(mh, cb_config, items_to_import):
    assert isinstance(mh, Message_Handler)
    assert isinstance(cb_config, dict)
    assert isinstance(items_to_import, set)
    rv = []

    cb_items = get_many_items(cb_config, items_to_import)
    for cb_item in cb_items:
        l_item = to_lobster(cb_config, cb_item)
        rv.append(l_item)

    return rv


def ensure_array_of_strings(instance):
    if (isinstance(instance, list) and
            all(isinstance(item, str)
                for item in instance)):
        return instance
    else:
        return [str(instance)]


def validate_authentication_parameters(cb_config, netrc_path=None):
    assert isinstance(cb_config, dict)
    assert netrc_path is None or isinstance(netrc_path, str)
    if (cb_config["token"] is None and
            (cb_config["user"] is None or cb_config["pass"] is None)):
        netrc_file = netrc_path or os.path.join(os.path.expanduser("~"),
                                                ".netrc")
        if os.path.isfile(netrc_file):
            netrc_config = netrc.netrc(netrc_file)
            machine = cb_config["root"][8:]
            auth = netrc_config.authenticators(machine)
            if auth is not None:
                print("Using .netrc login for %s" % cb_config["root"])
                cb_config["user"], _, cb_config["pass"] = auth
            else:
                provided_machine = ", ".join(netrc_config.hosts.keys()) or "None"
                sys.exit(f"Error parsing .netrc file."
                         f"\nExpected '{machine}', but got '{provided_machine}'.")

    if (cb_config["token"] is None and
            (cb_config["user"] is None or cb_config["pass"] is None)):
        sys.exit("lobster-codebeamer: please add your token to the config file, "
                 "or use user and pass in the config file, "
                 "or configure credentials in the .netrc file.")

    return cb_config


def parse_yaml_config(file_name: str):
    """
    Parses a YAML configuration file and returns a validated configuration dictionary.

    Args:
        file_name (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Parsed and validated configuration.

    Raises:
        ValueError: If `file_name` is not a string.
        FileNotFoundError: If the file does not exist.
        KeyError: If required fields are missing or unsupported keys are present.
    """
    assert isinstance(file_name, str)
    assert os.path.isfile(file_name)

    default_values = {
        'timeout': 30,
        'page_size': 100,
        'verify_ssl': False,
        'schema': 'Requirement',
    }

    required_fields = {"import_tagged", "import_query"}

    with open(file_name, "r", encoding='utf-8') as file:
        data = yaml.safe_load(file) or {}

    # Ensure at least one required field is present
    if not required_fields & data.keys():
        raise KeyError(f"One of the required fields "
                       f"must be present: {', '.join(required_fields)}")

    # Build the configuration dictionary
    json_config = {
        "references": {
            "refs": ensure_array_of_strings(data["refs"])
        } if "refs" in data else {},
        "token": data.pop("token", None),
        "base": f"{data.get('root', '')}/api/v3",
    }

    # Validate supported keys
    provided_config_keys = set(data.keys())
    unsupported_keys = provided_config_keys - SupportedConfigKeys.as_set()
    if unsupported_keys:
        raise KeyError(
            f"Unsupported config keys: {', '.join(unsupported_keys)}. "
            f"Supported keys are: {', '.join(SupportedConfigKeys.as_set())}."
        )

    # Merge with default values
    json_config.update({key: data.get(key, default_values.get(key))
                        for key in SupportedConfigKeys.as_set()})

    return json_config


ap = argparse.ArgumentParser(conflict_handler='resolve')


@get_version(ap)
def main():
    # lobster-trace: codebeamer_req.Dummy_Requirement
    ap.add_argument("--config",
                    help=("Path to YAML file with arguments, "
                          "by default (codebeamer-config.yaml) "
                          "supported references: '%s'" %
                          ', '.join(SupportedConfigKeys.as_set())),
                    default=os.path.join(os.getcwd(), "codebeamer-config.yaml"))

    ap.add_argument("--out",
                    help=("Name of output file"),
                    default="codebeamer.lobster")

    options = ap.parse_args()

    mh = Message_Handler()

    if not os.path.isfile(options.config):
        print((f"lobster-codebeamer: Config file '{options.config}' not found."))
        return 1

    cb_config = parse_yaml_config(options.config)

    if cb_config["out"] is None:
        cb_config["out"] = options.out

    if cb_config["root"] is None:
        sys.exit("lobster-codebeamer: Please set 'root' in the config file")

    if not cb_config["root"].startswith("https://"):
        sys.exit(f"Codebeamer root {cb_config['root']} must start with https://")

    cb_config = validate_authentication_parameters(cb_config)

    items_to_import = set()

    if cb_config.get("import_tagged"):
        if not os.path.isfile(cb_config["import_tagged"]):
            sys.exit(f"lobster-codebeamer: {cb_config['import_tagged']} is not a file.")
        items = {}
        try:
            lobster_read(mh       = mh,
                         filename = cb_config["import_tagged"],
                         level    = "N/A",
                         items    = items)
        except LOBSTER_Error:
            return 1
        for item in items.values():
            for tag in item.unresolved_references:
                if tag.namespace != "req":
                    continue
                try:
                    item_id = int(tag.tag, 10)
                    if item_id > 0:
                        items_to_import.add(item_id)
                    else:
                        mh.warning(item.location,
                                   "invalid codebeamer reference to %i" %
                                   item_id)
                except ValueError:
                    pass

    elif cb_config.get("import_query") is not None:
        try:
            if isinstance(cb_config["import_query"], str):
                if (cb_config["import_query"].startswith("-") and
                    cb_config["import_query"][1:].isdigit()):
                    ap.error("import_query must be a positive integer")
                elif cb_config["import_query"].startswith("-"):
                    ap.error("import_query must be a valid cbQL query")
                elif cb_config["import_query"] == "":
                    ap.error("import_query must either be a query string or a query ID")
                elif cb_config["import_query"].isdigit():
                    cb_config["import_query"] = int(cb_config["import_query"])
        except ValueError as e:
            ap.error(str(e))

    try:
        if cb_config.get("import_tagged"):
            items = import_tagged(mh, cb_config, items_to_import)
        elif cb_config["import_query"]:
            items = get_query(mh, cb_config, cb_config["import_query"])
    except LOBSTER_Error:
        return 1

    schema_config = get_schema_config(cb_config)

    if cb_config["out"] is None:
        with sys.stdout as fd:
            lobster_write(fd, schema_config["class"], "lobster_codebeamer", items)
    else:
        with open(cb_config["out"], "w", encoding="UTF-8") as fd:
            lobster_write(fd, schema_config["class"], "lobster_codebeamer", items)
        print(f"Written {len(items)} requirements to {cb_config['out']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
