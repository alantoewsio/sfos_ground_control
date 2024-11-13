""" SFOS Ground Control
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
import argparse as _args
import json
import os
from datetime import datetime, UTC
import yaml

from requests import Response
from requests.utils import dict_from_cookiejar as _dict_from_cookiejar

from sfos.base import (
    get_credential as _get_credential,
    GroundControlDB as _db,
)
from sfos.logging import logerror
from sfos.objects import FirewallInfo as _fwi, ServiceAddress as _sa
from sfos.webadmin import Connector


class AgentMethodsError(Exception):
    """Generic error raised by agent method calls"""


# @log_calls_decorator(Level.DEBUG, True, False)
def db_save_subs(db: _db | None = None, all_info: _fwi | None = None) -> None:
    """save to database

    Args:
        db (_db | None, optional): _description_. Defaults to None.
        all_info (_fwi | None, optional): _description_. Defaults to None.
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
def db_save_record(
    table: str,
    db: _db | None = None,
    **data,
) -> None:
    """Save to database

    Args:
        table (str): _description_
        db (_db | None, optional): _description_. Defaults to None.
    """
    if not db:
        return

    db.insert_into(
        table,
        timestamp=str(datetime.now(tz=UTC)),
        **data,
    )


# @log_calls_decorator(Level.DEBUG, True, False)
def db_save_info(
    db: _db | None = None,
    all_info: _fwi | None = None,
    address: _sa | None = None,
) -> None:
    """Save to database

    Args:
        db (_db | None, optional): _description_. Defaults to None.
        all_info (_fwi | None, optional): _description_. Defaults to None.
        address (_sa | None, optional): _description_. Defaults to None.
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
    result["fw_username"] = (
        args.username if args.username else os.environ.get("FW_USERNAME", "admin")
    )
    result["fw_password"] = (
        args.password if args.password else os.environ.get("FW_PASSWORD", None)
    )
    if args.use_vault:
        result["fw_password"] = _get_credential(
            mount_point=os.environ["VAULT_MOUNT_POINT"],
            secret_path=os.environ["VAULT_SECRET_PATH"],
            key=os.environ["VAULT_SECRET_KEY"],
        )
    return result


def _convert_inventory_to_connectors(inventory: list) -> list[Connector]:
    firewalls = []
    for fw in inventory:
        try:
            if "verify_tls" in fw:
                verify_tls = fw["verify_tls"]
            elif "verify-tls" in fw:
                verify_tls = fw["verify-tls"]
            else:
                verify_tls = True
            firewalls.append(
                Connector(
                    hostname=fw["hostname"],
                    port=fw["port"],
                    verify_tls=verify_tls,
                    username=fw["username"],
                    password=fw["password"],
                )
            )

        except Exception as e:
            logerror(f"Error reading inventory record {fw} - {e}")
    count = len(firewalls)
    print(f"{count} {"firewall" if count == 1 else "firewalls"} found in inventory")
    return firewalls


def _read_yaml_file(filename: str) -> dict:
    try:
        if filename is None:
            return None
        with open(filename, "r", encoding="utf-8") as fn:
            return yaml.safe_load(fn)
    except Exception as e:
        print(f"Error reading {filename} - {e}")


def _fill_missing_values_with_defaults(
    yaml_dict: list,
    hostname: str = "172.16.16.16",
    port: int = 4444,
    verify_tls: bool = True,
    username: str = None,
    password: str = None,
) -> list:

    for fw in yaml_dict:
        if "hostname" not in fw:
            fw["hostname"] = hostname
        if "port" not in fw:
            fw["port"] = port
        if "verify-tls" not in fw:
            fw["verify-tls"] = verify_tls
        if "username" not in fw:
            fw["username"] = username
        if "password" not in fw:
            fw["password"] = password
    return yaml_dict


def _parse_inv(
    yaml_dict: list | None,
    args: _args.Namespace,
    creds: dict,
) -> list:
    if yaml_dict is None:
        return []

    # return _fill_missing_values_with_defaults(
    #     yaml_dict,
    #     args.hostname,
    #     args.port,
    #     args.verift_tls,
    #     creds["fw_username"],
    #     creds["fw_password"],
    # )
    for fw in yaml_dict:
        if "hostname" not in fw:
            fw["hostname"] = args.hostname
        if "port" not in fw:
            fw["port"] = args.port
        if "verify-tls" not in fw:
            fw["verify-tls"] = args.verify_tls
        if "username" not in fw:
            fw["username"] = creds["fw_username"]
        if "password" not in fw:
            fw["password"] = creds["fw_password"]

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

    if args.hostname:
        # use a single firewall for this run
        print("using Hostname")
        fw_inventory.append(
            {
                "hostname": args.hostname,
                "port": args.port,
                "verify_tls": str(args.verify_tls).lower() == "true",
                "username": creds["fw_username"],
                "password": creds["fw_password"],
            },
        )
    elif args.inventory:
        fw_inventory = []
        for inv in args.inventory:
            yaml_list = _read_yaml_file(inv)
            fw_inventory = _combine_lists(
                _parse_inv(yaml_list, args, creds),
                fw_inventory,
            )
    else:
        print("no host found:", args.inventory, args.hostname)
    if not fw_inventory:
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
