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

import json
from sfos.base import GroundControlDB as _db
from sfos.webadmin import Connector


def run_query(
    firewalls: list[Connector],
    db: _db,
    field: str,
    operator: str,
    value: str,
    source: str = "fwinfo_latest",
) -> list:
    results = []
    for fw in firewalls:
        result = db.query_db(field, operator, value, source)
        results.append(result)

    return results


def format_results(results: list, indent: int = 2) -> str:
    return json.dumps(results, indent=indent)
