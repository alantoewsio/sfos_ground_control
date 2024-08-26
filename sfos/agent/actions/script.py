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
from sfos.agent.script_objs import load_script, execute_script
from sfos.webadmin.connector import Connector as _conn


def run_scripts(firewalls: list[_conn], args: _args.Namespace) -> list[dict]:
    results = []
    for fw in firewalls:
        for file in args.scripts:
            results.append(_script_do_run(fw, file))
    return results


def _script_do_run(fw: _conn, filename: str, state: dict | None = None) -> dict:
    try:
        scr = load_script(filename)
        result = execute_script(fw, scr)
        return {"fw": fw.address, "script": filename, "results": result}
    except Exception as e:
        print("run_script error: ", type(e), str(e), "file:", filename)
