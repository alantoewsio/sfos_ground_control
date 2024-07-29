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

from sfos.base.db import GroundControlDB as _db
from sfos.logging.logging import log, Level
from sfos.static import DATE_TIME_FMT as _DATE_FMT

db = _db()


fwinfo_table = [
    "address",
    "Model",
    "displayVersion",
    "version",
    "serial_number",
    "companyName",
    "username",
    "verify_tls",
    "message",
]

fwsubs_table = [
    "serial_number",
    "name",
    "start",
    "end",
    "timeframe",
]


def init_db(filename: str | None = None) -> _db:
    global db
    db = None
    if filename:
        log(Level.INFO, f"Initializing db '{filename}'")
        db = _db(filename)
    else:
        db = _db()
        log(Level.INFO, f"Initialized db '{db.filename}'")
    assert db  # GroundControlDB class is instantiated successfully

    if db.create_db():
        log(Level.INFO, f"New GroundControl database created: '{db.filename}'")

    if "inventory" not in db.list_tables():
        cols = {
            "address": "TEXT UNIQUE",
            "Model": "TEXT",
            "displayVersion": "TEXT",
            "version": "TEXT",
            "serial_number": "TEXT",
            "companyName": "TEXT",
            "username": "TEXT",
            "verify_tls": "TEXT",
            "message": "TEXT",
            "last_result": "TEXT DEFAULT ''",
            "consecutive_fails": "INTEGER DEFAULT 0",
            "reply_ms": "INTEGER DEFAULT -1",
            "added": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "last_seen": "TIMESTAMP DEFAULT NULL",
        }
        db.create_table("inventory", **cols)

    if "licenses" not in db.list_tables():
        cols = {
            "uid": "TEXT UNIQUE",
            "serial_number": "TEXT",
            "name": "TEXT",
            "start_date": "TIMESTAMP DEFAULT NULL",
            "expiry_date": "TIMESTAMP DEFAULT NULL",
            "bundle": "TEXT DEFAULT ''",
            "status": "TEXT DEFAULT ''",
            "deactivation_reason": "TEXT DEFAULT ''",
            "type": "TEXT DEFAULT ''",
            "added": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        }
        db.create_table("licenses", **cols)
        status_view = (
            "CREATE VIEW IF NOT EXISTS InventoryStatus AS "
            "SELECT address as Address, serial_number as 'Serial Number', "
            "model as Model, displayVersion as Version,companyName as Company, "
            "message as 'Error Message',last_result as Status,"
            f"strftime('{_DATE_FMT}', last_seen) as 'Last Seen', "
            "CAST (strftime('%j',current_timestamp) - strftime('%j',last_seen) AS INT) "
            "as 'Days Ago' "
            "WHERE 'Days Ago' > 90 "
            "ORDER BY last_result ASC, address"
        )
        db.execute(status_view)

    return db
