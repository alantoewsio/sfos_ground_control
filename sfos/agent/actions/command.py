"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

import argparse as _args
from sfos.agent.script_objs import ScriptItem, execute_script_item
from sfos.base import GroundControlDB as _db
from sfos.static import exceptions as _ex
from sfos.logging.logging import loginfo, logerror
from sfos.webadmin.connector import Connector as _conn, SfosResponse as _sresp


def run_cli_command(
    firewalls: list[_conn],
    args: _args.Namespace,
    state: dict | None = None,
    db: _db | None = None,
) -> list[_sresp]:
    """Run a command passed via the cli

    Args:
        firewalls (list[_conn]): _description_
        args (_args.Namespace): _description_
        state (dict | None, optional): _description_. Defaults to None.
        db (_db | None, optional): _description_. Defaults to None.
        print_results (bool, optional): _description_. Defaults to True.

    Returns:
        list[_sresp]: _description_
    """
    if args.command == "refresh":
        results = [run_command_refresh(fw, db) for fw in firewalls]
        return results
    else:
        loginfo("run_command_def args=", args=args)  # type: ignore
        results = []
        for fw in firewalls:
            try:
                results.extend(
                    run_command_def(
                        fw,
                        args.command,
                        args.object,
                        args.data,
                        state,
                    )
                )
            except Exception as e:
                logerror(e)
        return results


def run_command_refresh(fw: _conn, db: _db | None = None) -> _sresp:
    """Run a refresh command against the selected firewal"""
    if not db:
        return _sresp(
            error=_ex.DatabaseError(("No database")),
            trace="rcr-01",
        )

    msg = f"fetching info from {fw.address.address}.."  # type: ignore
    loginfo(msg, end="\r")
    sfos_resp = fw.get_info()
    loginfo(" " * len(msg), end="\r")

    db.insert_or_update_fwinfo(sfos_resp)
    sfos_resp.trace = "101"
    return sfos_resp


def run_command_def(
    fw: _conn,
    command: str,
    request_object: str | None = None,
    data: str | None = None,
    state: dict | None = None,
) -> list[_sresp]:
    """Run a command or command script against a firewall connection

    Args:
        fw (_conn): _description_
        command (str): _description_
        request_object (str | None, optional): _description_. Defaults to None.
        data (str | None, optional): _description_. Defaults to None.
        state (dict | None, optional): _description_. Defaults to None.

    Returns:
        list[_sresp]: _description_
    """
    if state:
        pass  # not implemented yet

    cmd = ScriptItem(command, request_object, data)
    return execute_script_item(fw, cmd)
