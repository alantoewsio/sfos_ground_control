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

import os
from datetime import datetime
import sqlite3
from pathlib import Path

from sfos.objects.firewall_info import FirewallInfo
from sfos.static import exceptions as _ex
from sfos.db import Database
from sfos.webadmin.connector import Connector as _conn, SfosResponse as _sresp
from sfos.logging import logtrace, logerror, loginfo

DEFAULT_SQL_INIT_PATH = "./sfos/base/db/init"


class GroundControlDB(Database):
    """A Database instance tailored for this application

    Args:
        Database (_type_): _description_
    """

    def __init__(self, filename: str | None = None):
        if not filename:
            filename = os.getenv("GC_DATABASE_FILE", "./ground_control.sqlite3")
        loginfo(f"Initializing database file '{filename}'")
        # Run database init scripts
        SQL_INIT_PATH = os.getenv("GC_SQL_INIT_PATH", DEFAULT_SQL_INIT_PATH)
        logtrace(f"fetching init scripts from  {SQL_INIT_PATH}")
        init_scripts = self.list_sql_files(SQL_INIT_PATH)
        logtrace(f"found {len(init_scripts)} sql init scripts: {init_scripts}")
        sql_init_scripts = [
            str(Path(SQL_INIT_PATH, file))
            for file in init_scripts
            # self.load_sql_from_file(file, path=SQL_INIT_PATH) for file in init_scripts
        ]
        super().__init__(filename, sql_init_scripts)

    def _prep_resp_for_inventory_update(self, sresp: _sresp) -> dict:
        """Format a dictionary with the firewall inventory info
        extracted from a SfosResponse"""

        success = sresp.success
        resp = getattr(sresp.data, "base_info", {})
        if success:
            last_result = "ONLINE"
        else:
            match type(sresp.error):
                case _ex.ConnectionTimeoutError:
                    last_result = "OFFLINE"
                case _ex.NameResolutionError:
                    last_result = "OFFLINE"
                case _:
                    last_result = "ERROR"
        data = {
            "address": sresp.fw.address.hostname,  # type: ignore
            "model": resp["Model"] if success else None,
            "displayVersion": resp["displayVersion"] if success else None,
            "version": resp["version"] if success else None,
            "serial_number": resp["serial_number"] if success else None,
            "companyName": resp["companyName"] if success else None,
            "username": resp["username"] if success else None,
            "verify_tls": sresp.fw.address.verify_tls,  # type: ignore
            "message": "" if success else sresp.text,
            "last_result": last_result,
            "consecutive_fails": 0,
            "reply_ms": sresp.timer if success else None,
            "updated": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat() if success else None,
        }
        return data

    def _prep_resp_for_license_update(self, sresp: _sresp) -> list[dict]:
        """Add a new license record to the database or updte an existing one

        Args:
            sresponse (_sresp): _description_
        """
        if not sresp.success:
            raise _ex.ResponseContentError("No license data in response")

        fwi = sresp.data
        assert isinstance(fwi, FirewallInfo)
        fw_license = fwi.get_license()
        entitlements = fw_license.__dict__()

        for sub in entitlements:
            sub["uid"] = sub["serial_number"] + sub["name"]
            sub["updated"] = datetime.now()

        return entitlements

    def load_sql_from_file(
        self, filename: str, path: str = "sfos/base/db/sql/"
    ) -> str | None:
        """Load the contents of a .sql file from 'path' folder.

        Args:
            filename (str): Filename of the sql file to load
            path (str, optional): Location to look for the file.
                                  Defaults to "sfos/base/db/sql/".
            default (str, optional): If the sql file does not exist,
                                    'default' wil be returned.
                                     Defaults to None.

        Returns:
            str: _description_
        """
        return super().load_sql_from_file(filename=filename, path=path)

    def insert_or_update_fwinfo(self, response: _sresp):
        """Attempt to insert an inventory record, and update the inventory if it

        Args:
            data (dict): _description_
            success (bool, optional): _description_. Defaults to True.
        """

        hostname = "NONE"
        try:
            assert isinstance(response.fw, _conn)
            if response.fw.address:
                hostname = response.fw.address.hostname
        finally:
            logtrace(
                host=hostname,
                response_success=response.success,
                response_error=response.error,  # type: ignore
                status_code=response.status_code,
            )
        inv_data = self._prep_resp_for_inventory_update(response)
        self.insert_or_update(
            insert_into="inventory",
            data=inv_data,
            on_conflict=["address"],
            increment=None if response.success else ["consecutive_fails"],
        )
        if response.success:
            lic_subs_data = self._prep_resp_for_license_update(response)
            for lic_data in lic_subs_data:
                try:
                    self.insert_or_update(
                        insert_into="licenses", data=lic_data, on_conflict=["uid"]
                    )
                except sqlite3.OperationalError as e:
                    logerror(error=str(e))
                except sqlite3.ProgrammingError as e:
                    logerror(error=str(e))

        else:
            logtrace("Skipping license import for ")

        return

    def get_inventory_status_query(self):
        """Called by command.py after refresh completes
        - this should be removed and switch to using query defined in qsl file

        Returns:
            _type_: _description_
        """
        sql = self.load_sql_from_file("inventory_insert_or_replace.sql")
        return self.select(raw_sql=sql)
        # return self.select(from_table="inventory_view")
