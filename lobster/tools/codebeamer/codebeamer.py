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
import time
import sys
import argparse
import netrc
from typing import List, Optional, Set, Union
from urllib.parse import quote, urlparse
from enum import Enum
import requests
import yaml

from lobster.items import Tracing_Tag, Requirement, Implementation, Activity
from lobster.location import Codebeamer_Reference
from lobster.errors import Message_Handler, LOBSTER_Error
from lobster.io import lobster_read, lobster_write
from lobster.meta_data_tool_base import MetaDataToolBase
from lobster.tools.codebeamer.bearer_auth import BearerAuth
from lobster.tools.codebeamer.config import AuthenticationConfig, Config
from lobster.tools.codebeamer.exceptions import (
    MismatchException, NotFileException, QueryException,
)


class SupportedConfigKeys(Enum):
    """Helper class to define supported configuration keys."""
    NUM_REQUEST_RETRY = "num_request_retry"
    RETRY_ERROR_CODES = "retry_error_codes"
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


def get_authentication(cb_auth_config: AuthenticationConfig) -> requests.auth.AuthBase:
    if cb_auth_config.token:
        return BearerAuth(cb_auth_config.token)
    return requests.auth.HTTPBasicAuth(cb_auth_config.user,
                                       cb_auth_config.password)


def query_cb_single(cb_config: Config, url: str):
    if cb_config.num_request_retry <= 0:
        raise ValueError("Retry is disabled (num_request_retry is set to 0). "
                         "Cannot proceed with retries.")

    for attempt in range(1, cb_config.num_request_retry + 1):
        try:
            result = requests.get(
                url,
                auth=get_authentication(cb_config.cb_auth_conf),
                timeout=cb_config.timeout,
                verify=cb_config.verify_ssl,
            )
            if result.status_code == 200:
                return result.json()

            if result.status_code in cb_config.retry_error_codes:
                print(f"[Attempt {attempt}/{cb_config.num_request_retry}] "
                      f"Retryable error: {result.status_code}")
                time.sleep(1)  # wait a bit before retrying
                continue

            print(f"[Attempt {attempt}/{cb_config.num_request_retry}] Failed with "
                  f"status {result.status_code}")
            break

        except requests.exceptions.ReadTimeout:
            print(f"[Attempt {attempt}/{cb_config.num_request_retry}] Timeout when "
                  f"fetching {url}")
        except requests.exceptions.RequestException as err:
            print(f"[Attempt {attempt}/{cb_config.num_request_retry}] Request error: "
                  f"{err}")
        break

    # Final error handling after all retries
    raise QueryException(f"Could not fetch {url}.")


def get_single_item(cb_config: Config, item_id: int):
    if not isinstance(item_id, int) or (item_id <= 0):
        raise ValueError("item_id must be a positive integer")
    url = f"{cb_config.base}/items/{item_id}"
    return query_cb_single(cb_config, url)


def get_many_items(cb_config: Config, item_ids: Set[int]):
    assert isinstance(item_ids, set)

    rv = []

    page_id = 1
    query_string = quote(f"item.id IN "
                         f"({','.join(str(item_id) for item_id in item_ids)})")

    while True:
        base_url = "%s/items/query?page=%u&pageSize=%u&queryString=%s"\
                   % (cb_config.base, page_id,
                      cb_config.page_size, query_string)
        data = query_cb_single(cb_config, base_url)
        rv += data["items"]
        if len(rv) == data["total"]:
            break
        page_id += 1

    return rv


def get_query(cb_config: Config, query: Union[int, str]):
    assert isinstance(query, (int, str))
    rv = []
    url = ""
    page_id = 1
    total_items = None

    while total_items is None or len(rv) < total_items:
        print("Fetching page %u of query..." % page_id)
        if isinstance(query, int):
            url = ("%s/reports/%u/items?page=%u&pageSize=%u" %
                    (cb_config.base,
                        query,
                        page_id,
                        cb_config.page_size))
        elif isinstance(query, str):
            url = ("%s/items/query?page=%u&pageSize=%u&queryString=%s" %
                    (cb_config.base,
                        page_id,
                        cb_config.page_size,
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
            raise MismatchException(
                f"Page mismatch in query result: expected page "
                f"{page_id} from codebeamer, but got {data['page']}"
            )

        if page_id == 1:
            total_items = data["total"]
        elif total_items != data["total"]:
            raise MismatchException(
                f"Item count mismatch in query result: expected "
                f"{total_items} items so far, but page "
                f"{data['page']} claims to have sent {data['total']} "
                f"items in total."
            )

        if isinstance(query, int):
            rv += [to_lobster(cb_config, cb_item["item"])
                    for cb_item in data["items"]]
        elif isinstance(query, str):
            rv += [to_lobster(cb_config, cb_item)
                    for cb_item in data["items"]]

        page_id += 1

    assert total_items == len(rv)

    return rv


def get_schema_config(cb_config: Config) -> dict:
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
    schema = cb_config.schema.lower()

    if schema not in schema_map:
        raise KeyError(f"Unsupported SCHEMA '{schema}' provided in configuration.")

    return schema_map[schema]


def to_lobster(cb_config: Config, cb_item: dict):
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
        cb_config.cb_auth_conf.root, item_name, kind)
    item = _create_lobster_item(
        schema_config["class"],
        common_params, item_name, status)

    if cb_config.references:
        for displayed_name in cb_config.references:
            if cb_item.get(displayed_name):
                item_references = cb_item.get(displayed_name) if (
                    isinstance(cb_item.get(displayed_name), list)) \
                    else [cb_item.get(displayed_name)]
            else:
                item_references = [value for custom_field
                                   in cb_item["customFields"]
                                   if custom_field["name"] == displayed_name and
                                   custom_field.get("values")
                                   for value in custom_field["values"]]

            for value in item_references:
                item.add_tracing_target(Tracing_Tag("req", str(value["id"])))

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


def import_tagged(cb_config: Config, items_to_import: Set[int]):
    assert isinstance(items_to_import, set)
    rv = []

    cb_items = get_many_items(cb_config, items_to_import)
    for cb_item in cb_items:
        l_item = to_lobster(cb_config, cb_item)
        rv.append(l_item)

    return rv


def ensure_list(instance) -> List:
    if isinstance(instance, list):
        return instance
    return [instance]


def update_authentication_parameters(
        auth_conf: AuthenticationConfig,
        netrc_path: Optional[str] = None):
    if (auth_conf.token is None and
            (auth_conf.user is None or auth_conf.password is None)):
        netrc_file = netrc_path or os.path.join(os.path.expanduser("~"),
                                                ".netrc")
        if os.path.isfile(netrc_file):
            netrc_config = netrc.netrc(netrc_file)
            machine = urlparse(auth_conf.root).hostname
            auth = netrc_config.authenticators(machine)
            if auth is not None:
                print(f"Using .netrc login for {auth_conf.root}")
                auth_conf.user, _, auth_conf.password = auth
            else:
                provided_machine = ", ".join(netrc_config.hosts.keys()) or "None"
                raise KeyError(f"Error parsing .netrc file."
                               f"\nExpected '{machine}', but got '{provided_machine}'.")

    if (auth_conf.token is None and
            (auth_conf.user is None or auth_conf.password is None)):
        raise KeyError("Please add your token to the config file, "
                       "or use user and pass in the config file, "
                       "or configure credentials in the .netrc file.")


def parse_yaml_config(file_name: str) -> Config:
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
    assert os.path.isfile(file_name)

    with open(file_name, "r", encoding='utf-8') as file:
        return parse_config_data(yaml.safe_load(file) or {})


def parse_config_data(data: dict) -> Config:
    # Validate supported keys
    provided_config_keys = set(data.keys())
    unsupported_keys = provided_config_keys - SupportedConfigKeys.as_set()
    if unsupported_keys:
        raise KeyError(
            f"Unsupported config keys: {', '.join(unsupported_keys)}. "
            f"Supported keys are: {', '.join(SupportedConfigKeys.as_set())}."
        )

    # create config object
    config = Config(
        references=ensure_list(data.get(SupportedConfigKeys.REFS.value, [])),
        import_tagged=data.get(SupportedConfigKeys.IMPORT_TAGGED.value),
        import_query=data.get(SupportedConfigKeys.IMPORT_QUERY.value),
        verify_ssl=data.get(SupportedConfigKeys.VERIFY_SSL.value, False),
        page_size=data.get(SupportedConfigKeys.PAGE_SIZE.value, 100),
        schema=data.get(SupportedConfigKeys.SCHEMA.value, "Requirement"),
        timeout=data.get(SupportedConfigKeys.TIMEOUT.value, 30),
        out=data.get(SupportedConfigKeys.OUT.value),
        num_request_retry=data.get(SupportedConfigKeys.NUM_REQUEST_RETRY.value, 5),
        retry_error_codes=data.get(SupportedConfigKeys.RETRY_ERROR_CODES.value, []),
        cb_auth_conf=AuthenticationConfig(
            token=data.get(SupportedConfigKeys.CB_TOKEN.value),
            user=data.get(SupportedConfigKeys.CB_USER.value),
            password=data.get(SupportedConfigKeys.CB_PASS.value),
            root=data.get(SupportedConfigKeys.CB_ROOT.value)
        ),
    )

    # Ensure consistency of the configuration
    if (not config.import_tagged) and (not config.import_query):
        raise KeyError(f"Either {SupportedConfigKeys.IMPORT_TAGGED.value} or "
                       f"{SupportedConfigKeys.IMPORT_QUERY.value} must be provided!")

    if config.cb_auth_conf.root is None:
        raise KeyError(f"{SupportedConfigKeys.CB_ROOT.value} must be provided!")

    if not config.cb_auth_conf.root.startswith("https://"):
        raise KeyError(f"{SupportedConfigKeys.CB_ROOT.value} must start with https://, "
                       f"but value is {config.cb_auth_conf.root}.")

    return config


class CodebeamerTool(MetaDataToolBase):
    def __init__(self):
        super().__init__(
            name="codebeamer",
            description="Extract codebeamer items for LOBSTER",
            official=True,
        )
        self._argument_parser.add_argument(
            "--config",
            help=(f"Path to YAML file with arguments, "
                  f"by default (codebeamer-config.yaml) "
                  f"supported references: '{', '.join(SupportedConfigKeys.as_set())}'"),
            default=os.path.join(os.getcwd(), "codebeamer-config.yaml"))

        self._argument_parser.add_argument(
            "--out",
            help=("Name of output file"),
            default="codebeamer.lobster",
        )

    def _run_impl(self, options: argparse.Namespace) -> int:
        try:
            return self._execute(options)
        except NotFileException as ex:
            print(ex)
        except QueryException as query_ex:
            print(query_ex)
            print("You can either:")
            print("* increase the timeout with the timeout parameter")
            print("* decrease the query size with the query_size parameter")
            print("* increase the retry count with the parameters (num_request_retry, "
                  "retry_error_codes)")
        return 1

    def _execute(self, options: argparse.Namespace) -> int:
        mh = Message_Handler()

        if not os.path.isfile(options.config):
            print((f"lobster-codebeamer: Config file '{options.config}' not found."))
            return 1

        cb_config = parse_yaml_config(options.config)

        if cb_config.out is None:
            cb_config.out = options.out

        update_authentication_parameters(cb_config.cb_auth_conf)

        items_to_import = set()

        if cb_config.import_tagged:
            if not os.path.isfile(cb_config.import_tagged):
                raise NotFileException(f"lobster-codebeamer: {cb_config.import_tagged} "
                                       f"is not a file.")
            items = {}
            try:
                lobster_read(
                    mh = mh,
                    filename = cb_config.import_tagged,
                    level = "N/A",
                    items = items,
                )
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
                                       f"invalid codebeamer reference to {item_id}")
                    except ValueError:
                        pass

        elif cb_config.import_query is not None:
            try:
                if isinstance(cb_config.import_query, str):
                    if (cb_config.import_query.startswith("-") and
                        cb_config.import_query[1:].isdigit()):
                        self._argument_parser.error(
                            "import_query must be a positive integer")
                    elif cb_config.import_query.startswith("-"):
                        self._argument_parser.error(
                            "import_query must be a valid cbQL query")
                    elif cb_config.import_query == "":
                        self._argument_parser.error(
                            "import_query must either be a query string or a query ID")
                    elif cb_config.import_query.isdigit():
                        cb_config.import_query = int(cb_config.import_query)
            except ValueError as e:
                self._argument_parser.error(str(e))

        try:
            if cb_config.import_tagged:
                items = import_tagged(cb_config, items_to_import)
            elif cb_config.import_query:
                items = get_query(cb_config, cb_config.import_query)
        except LOBSTER_Error:
            return 1

        schema_config = get_schema_config(cb_config)

        if cb_config.out is None:
            with sys.stdout as fd:
                lobster_write(fd, schema_config["class"], "lobster_codebeamer", items)
        else:
            with open(cb_config.out, "w", encoding="UTF-8") as fd:
                lobster_write(fd, schema_config["class"], "lobster_codebeamer", items)
            print(f"Written {len(items)} requirements to {cb_config.out}")

        return 0


def main() -> int:
    return CodebeamerTool().run()
