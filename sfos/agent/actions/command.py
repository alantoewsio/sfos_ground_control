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

import argparse as _args
import prettytable


from sfos.agent.script_objs import ScriptItem, execute_script_item
from sfos.base import GroundControlDB as _db
from sfos.webadmin.connector import Connector as _conn, SfosResponse as _sresp
from sfos.logging.logging import trace_calls, Level


@trace_calls(Level.INFO, False, False)
def run_command(
    firewalls: list[_conn],
    args: _args.Namespace,
    state: dict | None = None,
    db: _db | None = None,
    print_results: bool = True,
) -> list[_sresp]:
    if args.command == "refresh":
        results = [run_command_refresh(fw, db) for fw in firewalls]
        if print_results:
            query = db.query_inventory_status()
            records = query.get_cursor()
            table = prettytable.from_db_cursor(records)
            print(table)
        return [results]
    else:
        print("run_command_def args=", args)
        return [
            run_command_def(fw, args.command, args.object, args.data, state)
            for fw in firewalls
        ]


def run_command_refresh(fw: _conn, db: _db | None = None) -> _sresp:
    msg = f"fetching info from {fw.address.address}.."
    print(msg, end="\r")
    sfos_resp = fw.get_info()
    print(" " * len(msg), end="\r")
    db.add_or_update_inventory(fw, sfos_resp)
    db.add_or_update_license(sfos_resp)

    return _sresp(
        fw=fw,
        request=sfos_resp.request,
        response=sfos_resp.response,
        error=sfos_resp.error,
        data=sfos_resp.data,
        timer=sfos_resp.timer,
        traceval="101",
    )


def run_command_def(
    fw: _conn,
    command: str,
    request_object: str | None = None,
    data: str | None = None,
    state: dict | None = None,
) -> list[_sresp]:
    cmd = ScriptItem(command, request_object, data)
    return execute_script_item(fw, cmd)
