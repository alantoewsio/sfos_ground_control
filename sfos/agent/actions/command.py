""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing
permissions and limitations under the License.
"""

import argparse
import json
from datetime import datetime, UTC

from sfos.agent.methods import db_save_record as _db_save_record
from sfos.agent.script_objs import ScriptItem, ScriptItemResponse, execute_script_item
from sfos.base import FirewallInfo as _fwi, GroundControlDB as _db
from sfos.webadmin.connector import Connector


def run_command(
    firewalls: list[Connector], args: argparse.Namespace, db: _db | None = None
) -> list:
    results = []

    if args.command == "refresh":
        results.extend([run_command_refresh(fw) for fw in firewalls])
    else:
        results.extend(
            [
                run_command_def(fw, args.command, args.object, args.data)
                for fw in firewalls
            ]
        )

    _file_save_results(json.dumps(results, indent=2), args.write_to_file, args.append)
    return results


def run_command_refresh(fw: Connector, db: _db) -> _fwi | None:
    try:
        all_info = fw.get_info()
        if not all_info:
            print(f"No results from {fw.address}")
            return None
        _db_save_info_and_subs(fw, all_info, db)
        return all_info.base_info + all_info.license_dict

    except TypeError:
        pass

    except Exception as e:
        message = f"ERROR ({type(e)}) {str(e)}"
        print(message)
        db.insert_into(
            "fwinfo",
            timestamp=str(datetime.now(tz=UTC)),
            address=fw.address.url_base,
            verify_tls=fw.address.verify_tls,
            message=message,
        )


def run_command_def(
    fw: Connector,
    command: str,
    request_object: str | None = None,
    data: str | None = None,
) -> list[ScriptItemResponse]:
    cmd = ScriptItem(command, request_object, data)
    results = execute_script_item(fw, cmd)
    return results


def _db_save_info_and_subs(fw: Connector, info: _fwi, db: _db | None) -> None:
    if not db:
        return
    _db_save_record(
        "fwinfo",
        db,
        address=fw.address.url_base,
        verify_tls=fw.address.verify_tls,
        **info.basic_info,
    )
    _db_save_record("fwsubs", db, info.license_dict)


def _file_save_results(results: str, filename: str, append: bool) -> None:
    try:
        writer = open(filename, "a" if append else "w")
        writer.write(json.dumps(results, indent=2))
    except Exception as e:
        print("Error writing outpot file: ", filename, "error:", str(e))
