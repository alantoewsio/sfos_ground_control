"""SFOS Ground Control.

Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

# pylint: disable=broad-exception-caught
from __future__ import annotations

import argparse as _args
import csv
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import yaml
from requests import Response
from requests.utils import dict_from_cookiejar as _dict_from_cookiejar

from sfos.base import (
    GroundControlDB as _Db,
)
from sfos.base import (
    get_credential as _get_credential,
)
from sfos.logging import logdebug, logerror, loginfo
from sfos.objects import FirewallInfo as _Fwi
from sfos.objects import ServiceAddress as _Sa
from sfos.webadmin import Connector


class AgentMethodsError(Exception):
    """Generic error to be raised by agent method calls."""


# @log_calls_decorator(Level.DEBUG, True, False)
def db_save_subs(db: _Db | None = None, all_info: _Fwi | None = None) -> None:
    """Save subscription info to database.

    Args:

        db (_Db | None, optional): _description_. Defaults to None.
        all_info (_Fwi | None, optional): _description_. Defaults to None.

    """
    if not (db or all_info):
        return
    subs = all_info.subscription_list
    for sub in subs:
        db.insert_into(
            "fwsubs",
            timestamp=str(datetime.now(tz=UTC)),
            serial_number=all_info.applianceKey,
            **sub,
        )


# @log_calls_decorator(Level.DEBUG, True, False)
def db_Save_record(
    table: str,
    db: _Db | None = None,
    **data,
) -> None:
    """Save to database

    Args:
        table (str): _description_
        db (_Db | None, optional): _description_. Defaults to None.
    """
    if not db:
        return

    db.insert_into(
        table,
        timestamp=str(datetime.now(tz=UTC)),
        **data,
    )


# @log_calls_decorator(Level.DEBUG, True, False)
def db_Save_info(
    db: _Db | None = None,
    all_info: _Fwi | None = None,
    address: _Sa | None = None,
) -> None:
    """Save to database

    Args:
        db (_Db | None, optional): _description_. Defaults to None.
        all_info (_Fwi | None, optional): _description_. Defaults to None.
        address (_Sa | None, optional): _description_. Defaults to None.
    """
    if not (db or address or all_info):
        return
    fwinfo = all_info.base_info
    fwinfo.pop("subscriptions", None)
    db.insert_into(
        "fwinfo",
        timestamp=str(datetime.now(tz=UTC)),
        address=address.url_base,
        verify_tls=address.verify_tls,
        **fwinfo,
    )


def process_state_variables(raw_script: str, state: dict | None = None) -> str:
    """Replaces placeholder {variable} srings in raw_script with values of matching
    keys in state dict, if present
    Accepts:
      raw_script: str  raw text contents of script to be run
      state: dict      a dict containing variable keys and replacement values
    """
    result = raw_script
    if r"{state." in raw_script:
        for k in state.items():
            result = result.format({f"state.{k}", state[k]})
    return result


def load_json_data(filename: str, state: dict | None = None) -> dict | list:
    """Load json data from file

    Args:
        filename (str): _description_
        state (dict | None, optional): _description_. Defaults to None.

    Returns:
        dict | list: _description_
    """
    json_str = load_file_str(filename)
    if state:
        json_str = process_state_variables(json_str, state)

    json_obj = json.loads(json_str)
    return json_obj


def load_file_str(filename: str) -> str:
    """Accepts:
    filename: str   The name of a file to be opened

    Returns:
    File contents as SfosRequest Definition
    """
    try:
        contents: str | None = None
        with open(filename, encoding="utf-8") as f:
            contents = f.read()
        return contents

    except FileNotFoundError as e:
        raise FileNotFoundError from e

    except Exception as e:
        raise AgentMethodsError from e


def read_cred_args(args: _args.Namespace) -> dict:
    """_summary_

    Args:
        args (_args.Namespace): _description_

    Returns:
        dict: _description_
    """
    result = {}
    env_user = os.environ.get("FW_USERNAME", None)
    if args.username:
        logdebug("Found username in args:", args.username)
        result["fw_username"] = args.username
    elif env_user:
        logdebug("Found username in env:FW_USERNAME: ", env_user)
        result["fw_username"] = env_user
    else:
        logdebug("Using default username choice: admin")

    env_pass = os.environ.get("FW_PASSWORD", None)
    if args.password:
        logdebug(f"Found password in args: len({len(args.password)})")
        if args.password:
            result["fw_password"] = args.password
    elif env_pass:
        logdebug(f"Found password in 'env:FW_PASSWORD': len={len(env_pass)}")
        result["fw_password"] = env_pass
    elif args.use_vault:
        vault_pass = _get_credential(
            mount_point=os.environ["VAULT_MOUNT_POINT"],
            secret_path=os.environ["VAULT_SECRET_PATH"],
            key=os.environ["VAULT_SECRET_KEY"],
        )
        if vault_pass:
            logdebug(
                f"Found password in vault path {os.environ['VAULT_SECRET_PATH']}: "
                f"len={len(vault_pass)}"
            )
            result["fw_password"] = vault_pass

    return result


def _convert_inventory_to_connectors(inventory: list) -> list[Connector]:
    firewalls = []
    for fw in inventory:
        try:
            # if "verify_tls" in fw:
            #     verify_tls = fw["verify_tls"]
            # elif "verify-tls" in fw:
            #     verify_tls = fw["verify-tls"]
            # else:
            #     verify_tls = True
            firewalls.append(
                Connector(**fw)
                #     hostname=fw["hostname"],
                #     port=fw["port"],
                #     verify_tls=verify_tls,
                #     username=fw["username"],
                #     password=fw["password"],
                # )
            )
        except Exception as e:
            logerror(f"Error reading inventory record {fw} - {e}")
    count = len(firewalls)
    logdebug(f"{count} {'firewall' if count == 1 else 'firewalls'} found in inventory")
    return firewalls


def _read_inv_file(filename: str) -> list | None:
    filepath = Path(filename)
    if not filepath.is_file():
        print(f"{filename} not found.")
        return None

    file_extension = filepath.suffix
    try:
        results = None
        if file_extension in {".yml", ".yaml"}:
            results = _read_yaml_file(filename)
        elif file_extension == ".csv":
            results = _read_csv_file(filename)
        elif file_extension == ".json":
            results = _read_json_file(filename)
        else:
            print("Inventory file type unrecognized.")
            return None
        logdebug(
            f"loaded {file_extension} file '{filename}' and found {len(results)} entries."
        )
        return results

    except Exception as e:
        print(f"Error reading {file_extension} {filename} - {e}")


def _read_json_file(filepath: str) -> list[dict]:
    with open(filepath, mode="r") as fn:
        return json.load(fn)


def convert_value(value):
    value = value.strip()
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def _read_csv_file(filepath: str) -> list[dict]:
    result = []
    EMPTY = ""
    with open(filepath, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Skip the row if all values are empty (ignoring whitespace)
            if not any(value.strip() for value in row.values()):
                continue
            processed_row = {
                key.strip(): convert_value(value)
                for key, value in row.items()
                if value is not EMPTY
            }
            result.append(processed_row)
    return result


def _read_yaml_file(filepath: str) -> list[dict]:
    if filepath is None:
        return None
    with open(filepath, "r", encoding="utf-8") as fn:
        return yaml.safe_load(fn)


def _parse_inv(
    yaml_dict: list[dict] | None,
    args: _args.Namespace,
    creds: dict,
) -> list:
    if yaml_dict is None:
        return []

    allowed_keys = ["hostname", "port", "username", "password", "verify_tls", "timeout"]

    # Make sure creds dict contains expected keys
    creds["fw_username"] = creds.pop("fw_username", "admin")
    creds["fw_password"] = creds.pop("fw_password", None)

    for fw in yaml_dict:
        # Make sure that fw dict contains all required keys
        fw["hostname"] = fw.pop("hostname", args.hostname)
        fw["port"] = fw.pop("port", args.port)
        fw["verify_tls"] = fw.pop(
            "verify_tls", fw.pop("verify-tls", args.verify_tls or True)
        )
        fw["username"] = fw.pop("username", creds["fw_username"])
        fw["password"] = fw.pop("password", creds["fw_password"])
        fw["timeout"] = fw.pop("timeout", 2)

        # find any unsupported keys that should be removed
        remove_keys = [key for key in fw.keys() if key not in allowed_keys]

        # drop and announce all unexpected keys
        for key in remove_keys:
            message = f"removing unexpected key '{key}' from {fw['hostname']}"
            print(message)
            loginfo(message)
            fw.pop(key, None)

    return yaml_dict


def _combine_lists(source: list, dest: list) -> list:
    for src_item in source:
        if src_item not in dest:
            dest.append(src_item)
    return dest


def read_firewall_inventory(args: _args.Namespace, creds: dict) -> list[Connector]:
    """read inventory args

    Args:
        args (_args.Namespace): _description_
        creds (dict): _description_

    Raises:
        Exception: _description_

    Returns:
        list[Connector]: _description_
    """
    fw_inventory = []
    verify_tls = False if args.insecure else str(args.verify_tls).lower() == "true"
    if args.hostname:
        # use a single firewall for this run
        for hostname in args.hostname:
            fw_inventory.append(
                {
                    "hostname": hostname,
                    "port": args.port,
                    "verify_tls": verify_tls,
                    "username": creds["fw_username"],
                    "password": creds["fw_password"],
                },
            )
        print("Loaded firewall inventory from args")
    elif args.inventory:
        fw_inventory = []
        for inv in args.inventory:
            inv_list = _read_inv_file(inv)
            fw_inventory = _combine_lists(
                _parse_inv(inv_list, args, creds),
                fw_inventory,
            )
        logdebug("Loaded firewall inventory from file")
    elif args.version:
        logdebug("Performing agent version check")
    else:
        # no host was found in inventory
        # print("no host found:", args.inventory, args.hostname)
        pass
    if not fw_inventory and not args.version:
        raise AgentMethodsError("A hostname or firewall inventory file is required")

    firewalls = _convert_inventory_to_connectors(fw_inventory)
    return firewalls


def response_to_dict(response: Response, _root: bool = True):
    """covert to dict for portability

    Args:
        response (Response): _description_
        _root (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    response_dict = {}
    try:
        response_dict = {
            "text": response.text,
            "headers": dict(sorted(response.headers.items())),
            "cookies": dict(sorted(_dict_from_cookiejar(response.cookies).items())),
            "status_code": response.status_code,
            "request": {
                "url": response.request.url,
                "method": response.request.method,
                "headers": dict(sorted(response.request.headers.items())),
                "path_url": response.request.path_url,
                "body": response.request.body,
            },
        }
        if _root:
            response_dict["history"] = [
                response_to_dict(h, False) for h in response.history
            ]

    except Exception as e:
        msg = f"resp2dict Exception: type='{type(e)}' msg='{e}'"
        print(msg)
        response_dict["exception"] = msg
    return response_dict
