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

from datetime import datetime
import os
import pytest

from sfos.base import GroundControlDB as DB, init_db


@pytest.fixture
def dbname() -> str:
    return "./test/temp/test_30_gcdb.sqlite3"


@pytest.fixture
def t_db(dbname: str):
    # global db
    cleanup(dbname)
    db = init_db(filename=dbname)
    assert os.path.exists(dbname)
    yield db
    db.close_connection()
    db = None
    cleanup(dbname, assert_fail=False)


@pytest.fixture
def fwinfo_good() -> dict:
    return {
        "address": "test.firewall.1",
        "Model": "SFVUNL",
        "displayVersion": "19.5 MR-3",
        "version": "19.5.3.100",
        "serial_number": "X123456789012",
        "companyName": "Test Inc.",
        "username": "testuser",
        "verify_tls": True,
        "message": None,
    }


@pytest.fixture
def fwinfo_bad() -> dict:
    return {
        "address": "test.firewall.2",
        "Model": None,
        "displayVersion": None,
        "version": None,
        "serial_number": None,
        "companyName": None,
        "username": None,
        "verify_tls": None,
        "message": (
            "ERROR (<class 'sfos.base.exceptions.LoginError'>) "
            "Authentication failed - Unexpected response"
        ),
    }


def cleanup(dbname: str, assert_fail: bool = True) -> None:
    if os.path.exists(dbname):
        print(f"removing {dbname}")
        os.remove(dbname)
        if assert_fail:
            assert not os.path.exists(dbname)
        print(f"remove '{dbname}' result: {not os.path.exists(dbname)}")
    else:
        print(f"'{dbname}' doesn't exist. no cleanup needed.")


def test_init_db_tables(t_db: DB) -> None:
    e_tbls = ["version", "inventory", "sqlite_sequence", "licenses"]
    t_tbls = t_db.list_tables()
    assert t_tbls == e_tbls


def test_init_db_fwinfo_columns(t_db: DB) -> None:
    e_cols = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "address", "TEXT", 0, None, 0),
        (2, "Model", "TEXT", 0, None, 0),
        (3, "displayVersion", "TEXT", 0, None, 0),
        (4, "version", "TEXT", 0, None, 0),
        (5, "serial_number", "TEXT", 0, None, 0),
        (6, "companyName", "TEXT", 0, None, 0),
        (7, "username", "TEXT", 0, None, 0),
        (8, "verify_tls", "TEXT", 0, None, 0),
        (9, "message", "TEXT", 0, None, 0),
        (10, "last_result", "TEXT", 0, "''", 0),
        (11, "consecutive_fails", "INTEGER", 0, "0", 0),
        (12, "reply_ms", "INTEGER", 0, "-1", 0),
        (13, "added", "TIMESTAMP", 0, "CURRENT_TIMESTAMP", 0),
        (14, "updated", "TIMESTAMP", 0, "CURRENT_TIMESTAMP", 0),
        (15, "last_seen", "TIMESTAMP", 0, "NULL", 0),
    ]

    t_cols = t_db.list_table_col_defs("inventory")
    assert t_cols == e_cols


def test_init_db_licenses_columns(t_db: DB) -> None:
    e_cols = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "uid", "TEXT", 0, None, 0),
        (2, "serial_number", "TEXT", 0, None, 0),
        (3, "name", "TEXT", 0, None, 0),
        (4, "start_date", "TIMESTAMP", 0, "NULL", 0),
        (5, "expiry_date", "TIMESTAMP", 0, "NULL", 0),
        (6, "bundle", "TEXT", 0, "''", 0),
        (7, "status", "TEXT", 0, "''", 0),
        (8, "deactivation_reason", "TEXT", 0, "''", 0),
        (9, "type", "TEXT", 0, "''", 0),
        (10, "added", "TIMESTAMP", 0, "CURRENT_TIMESTAMP", 0),
        (11, "updated", "TIMESTAMP", 0, "CURRENT_TIMESTAMP", 0),
    ]
    t_cols = t_db.list_table_col_defs("licenses")
    assert t_cols == e_cols


def test_query(t_db: DB, fwinfo_good: dict, fwinfo_bad: dict) -> None:
    snbase = "X1234567890"

    for y in range(1, 3):
        for x in range(1, 11):
            sn = snbase + f"{y:01n}{x:02n}"
            data = {
                "address": f"G{y:01n}{x:02n}.good.test.firewall",
                "serial_number": sn,
                "model": "XGS2300",
                "displayVersion": "SFOS 20.0.0 GA-Build222",
                "version": "20.0.0.222",
                "companyName": "test company Inc.",
                "username": "tester",
                "verify_tls": True,
                "message": "",
                "consecutive_fails": 0,
                "updated": datetime.now(),
                "last_result": "ONLINE",
                "last_seen": datetime.now(),
                "reply_ms": "100",
            }
            t_db._add_or_update_inventory(data)

        for x in range(1, 6):
            sn = snbase + f"{y:01n}{x:02n}"
            data = {
                "address": f"B{y:01n}{x:02n}.good.test.firewall",
                "serial_number": sn,
                "model": "XGS2300",
                "displayVersion": "SFOS 20.0.0 GA-Build222",
                "version": "20.0.0.222",
                "companyName": "test company Inc.",
                "username": "tester",
                "verify_tls": True,
                "message": "Login Failure",
                "consecutive_fails": 0,
                "updated": datetime.now(),
                "last_result": "ERROR",
                "last_seen": datetime.now(),
                "reply_ms": "100",
            }
            t_db._add_or_update_inventory(data)

    result = (
        t_db.select(from_table="inventory").where("address", "like", "test").fetchall()
    )

    assert len(result) == 30
