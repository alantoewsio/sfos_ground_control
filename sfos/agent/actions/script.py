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

from requests import Response
from sfos.agent.script_objs import load_script, execute_script
from sfos.webadmin.connector import Connector


def run_scripts(*files: str) -> list[list[Response]]:
    results = []
    for file in files:
        results.append(_script_do_run(file))
    return results


def _script_do_run(
    fw: Connector, filename: str, state: dict | None = None
) -> list[Response]:
    try:
        scr = load_script(filename)
        result = execute_script(fw, scr, state)
        return result
    except Exception as e:
        print("run_script error: ", type(e), str(e), "file:", filename)
