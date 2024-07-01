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
from datetime import datetime

import prettytable
from sfos.agent.methods import db_save_record as _db_save_record
from sfos.agent.script_objs import ScriptItem, execute_script_item
from sfos.base import GroundControlDB as _db
from sfos.webadmin.connector import Connector as _conn, SfosResponse as _sresp


def run_command(
    firewalls: list[_conn],
    args: _args.Namespace,
    db: _db | None = None,
    print_results: bool = True,
) -> list[_sresp]:
    if args.command == "refresh":
        results = [run_command_refresh(fw, db) for fw in firewalls]
        if print_results:
            query = db.select(
                "address",
                "serial_number",
                "model",
                "displayVersion",
                "companyName",
                "message",
                "last_result",
                "strftime('%d-%m-%Y', (last_seen/1000)) AS 'last update'",
                from_table="inventory",
            )
            records = query.get_cursor()
            table = prettytable.from_db_cursor(records)
            print(table)
        return results
    else:
        return [
            run_command_def(fw, args.command, args.object, args.data)
            for fw in firewalls
        ]


def run_command_refresh(
    fw: _conn, db: _db | None = None, print_results: bool = True
) -> _sresp:
    tstart = datetime.now()
    sresp = fw.get_info()
    tstop = datetime.now()
    tdiff = tstop - tstart
    int(tdiff.microseconds / 1000)
    print(".", end="")

    if db:
        _db_save_info_and_subs(sresp, db)

    if sresp.success:
        sresp.data = sresp.data.base_info
        sresp.data["last_result"] = "ONLINE"
        sresp.data["last_seen"] = tstop
    else:
        sresp.data = {}
        sresp.data["last_result"] = "OFFLINE"
        sresp.data["message"] = sresp.text

    sresp.data["address"] = fw.address.hostname
    sresp.data["reply_ms"] = int(tdiff.microseconds / 1000)
    sresp.data["updated"] = tstop
    db.upsert(
        "inventory",
        "address",
        sresp.fw.address.hostname,
        **sresp.data,
    )

    return _sresp(
        fw=fw,
        request=sresp.request,
        response=sresp.response,
        error=sresp.error,
        data=sresp.data,
        trace="101",
    )


def run_command_def(
    fw: _conn,
    command: str,
    request_object: str | None = None,
    data: str | None = None,
) -> list[_sresp]:
    cmd = ScriptItem(command, request_object, data)
    return execute_script_item(fw, cmd)


def _db_save_info_and_subs(sresp: _sresp, db: _db | None) -> None:
    if not db:
        return
    if sresp.success:
        # save fwinfo
        _db_save_record(
            "fwinfo",
            db,
            address=sresp.fw.address.address,
            verify_tls=sresp.fw.address.verify_tls,
            **sresp.data.base_info,
        )

        # save fwsubs
        [
            _db_save_record("fwsubs", db, **sub)
            for sub in sresp.data.subscription_list
            if sub["end"]
        ]
    else:
        db.insert_into(
            "fwinfo",
            timestamp=sresp.timestamp,
            address=sresp.fw.address.url_base,
            verify_tls=sresp.fw.address.verify_tls,
            message=sresp.text,
        )
