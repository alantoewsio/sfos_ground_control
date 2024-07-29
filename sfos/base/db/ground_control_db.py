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

import os
from datetime import datetime

from sfos.static import exceptions as _ex
from sfos.db import Database
from sfos.static import DATE_TIME_FMT as _DATE_TIME_FMT
from sfos.webadmin.connector import Connector, SfosResponse as _sresp


class GroundControlDB(Database):

    def __init__(self, filename: str | None = None):
        if not filename:
            filename = os.getenv("GROUND_CONTROL_DB_KEY", "./ground_control.sqlite3")
        super().__init__(filename)

    def add_or_update_license(self, sfos_response: _sresp) -> None:
        if not sfos_response.success:
            return
        fwi = sfos_response.data
        fw_license = fwi.get_license()
        entitlements = fw_license.__dict__()

        for sub in entitlements:
            sub["uid"] = sub["serial_number"] + sub["name"]
            sub["updated"] = datetime.now()
            self.partial_update("licenses", ["serial_number", "name"], **sub)

    def add_or_update_inventory(self, fw: Connector, sfos_resp: _sresp) -> None:
        data = {}
        if sfos_resp.success:
            data = sfos_resp.data.base_info
            data["last_result"] = "ONLINE"
            data["last_seen"] = datetime.now()
            data["message"] = ""
            data["consecutive_fails"] = 0

        else:
            data = {}
            match type(sfos_resp.error):
                case _ex.ConnectionTimeoutError:
                    data["last_result"] = "OFFLINE"
                case _ex.NameResolutionError:
                    data["last_result"] = "OFFLINE"
                case _:
                    data["last_result"] = "ERROR"

            data["message"] = sfos_resp.text
            data["consecutive_fails"] = "<INCREMENT>"

        data["address"] = fw.address.hostname
        data["reply_ms"] = sfos_resp.timer
        data["updated"] = datetime.now()
        self._add_or_update_inventory(data)

    def _add_or_update_inventory(self, data: dict):
        self.partial_update("inventory", "address", **data)

    def query_inventory_status(self):
        return (
            self.select(
                "address as Address",
                "serial_number as 'Serial Number'",
                "model as Model",
                "displayVersion as Version",
                "companyName as Company",
                "message as 'Error Message'",
                "last_result as Status",
                f"strftime('{_DATE_TIME_FMT}', last_seen) as 'Last Seen Date' ",
                (
                    "CAST ("
                    "strftime('%j',current_timestamp) - "
                    "strftime('%j',last_seen) "
                    "AS INT) as 'Days Ago' "
                ),
                from_table="inventory",
            )
            .order_by("'Last Seen Date'", ascending=False, nulls_first=False)
            .order_by("Status")
        )
