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
import pytest

from sfos.agent import init_db  # , db
from sfos.base import GroundControlDB as DB


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
    e_tbls = ["version", "inventory", "sqlite_sequence", "fwinfo", "fwsubs"]
    t_tbls = t_db.list_tables()
    assert t_tbls == e_tbls


def test_init_db_views(t_db: DB) -> None:
    e_views = ["fwinfo_latest", "fwinfo_missing"]
    t_views = t_db.list_views()
    assert t_views == e_views


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
        (10, "timestamp", "TEXT", 0, None, 0),
    ]

    t_cols = t_db.list_table_col_defs("fwinfo")
    assert t_cols == e_cols


def test_init_db_fwsubs_columns(t_db: DB) -> None:
    e_cols = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "serial_number", "TEXT", 0, None, 0),
        (2, "name", "TEXT", 0, None, 0),
        (3, "start", "TEXT", 0, None, 0),
        (4, "end", "TEXT", 0, None, 0),
        (5, "timeframe", "TEXT", 0, None, 0),
        (6, "timestamp", "TEXT", 0, None, 0),
    ]
    t_cols = t_db.list_table_col_defs("fwsubs")
    assert t_cols == e_cols


def test_query(t_db: DB, fwinfo_good: dict, fwinfo_bad: dict) -> None:
    snbase = "X123456789012"
    for y in range(1, 3):
        for x in range(1, 11):
            sn = snbase + f"{x:02n}"
            fwinfo_good["address"] = f"{x}.good.test.firewall"
            fwinfo_good["serial_number"] = sn
            t_db.insert_into("fwinfo", **fwinfo_good)

        for x in range(1, 6):
            sn = snbase + f"{x:02n}"
            fwinfo_bad["address"] = f"{x}.bad.test.firewall"
            fwinfo_bad["serial_number"] = sn
            t_db.insert_into("fwinfo", **fwinfo_bad)

    result = t_db.query_db("address", "like", "test", "fwinfo")
    assert len(result) == 30
    result = t_db.query_db("address", "like", "test", "fwinfo_latest")
    assert len(result) == 10
    result = t_db.query_db("address", "like", "test", "fwinfo_missing")
    assert len(result) == 5
