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

from sfos.base import GroundControlDB as _db

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
        # print(f"Initializing db '{filename}'")
        db = _db(filename)
    else:
        db = _db()
        # print(f"Initialized db '{db.filename}'")
    assert db  # GroundControlDB class is instantiated successfully

    if db.create_db():
        print(f"New GroundControl database created: '{db.filename}'")

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
            "last_result": "TEXT DEFAULT 'none'",
            "reply_ms": "INTEGER DEFAULT -1",
            "added": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "last_seen": "TIMESTAMP DEFAULT NULL",
        }
        db.create_table("inventory", **cols)

    if "fwinfo" not in db.list_tables():
        # print("creating fwinfo table")
        cols = {k: "TEXT" for k in fwinfo_table}
        cols["timestamp"] = "TEXT"
        db.create_table("fwinfo", **cols)

    if "fwsubs" not in db.list_tables():
        # print("creating fwsubs table")
        cols = {k: "TEXT" for k in fwsubs_table}
        cols["timestamp"] = "TEXT"
        db.create_table("fwsubs", **cols)

    SQL = """CREATE VIEW IF NOT EXISTS fwinfo_latest AS
    SELECT * FROM fwinfo
    WHERE fwinfo.ID in (select UID from(
    SELECT max(fi1.id) as UID, fi1.serial_number
    FROM fwinfo as fi1
    WHERE fi1.version IS NOT NULL
    GROUP BY fi1.serial_number))"""
    db.execute(SQL)

    SQL = """CREATE VIEW IF NOT EXISTS fwinfo_missing AS
    SELECT * FROM fwinfo
    WHERE fwinfo.ID in (select UID from(
    SELECT max(fi1.id) as UID, fi1.address
    FROM fwinfo as fi1
    WHERE fi1.version IS NULL
    GROUP BY fi1.address))"""

    db.execute(SQL)
    return db
