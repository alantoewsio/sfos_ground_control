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

from sfos.base import GroundControlDB as DB


@pytest.fixture
def dbname() -> str:
    return "./test/temp/test_13_gcdb.sqlite3"


@pytest.fixture
def t_db(dbname: str):
    dbname = "./test/temp/test_13_gcdb.sqlite3"
    cleanup(dbname)
    db = DB(filename=dbname)
    db.create_db()
    assert os.path.exists(dbname)
    yield db
    db.close_connection()
    db = None
    cleanup(dbname, assert_fail=False)


def t_get_db(dbname: str):
    dbname = "./test/temp/test_13_gcdb.sqlite3"
    cleanup(dbname)
    db = DB(filename=dbname)
    db.create_db()
    assert os.path.exists(dbname)
    return db


def cleanup(dbname: str, assert_fail: bool = True) -> None:
    if os.path.exists(dbname):
        print(f"removing {dbname}")
        os.remove(dbname)
        if assert_fail:
            assert not os.path.exists(dbname)
        print(f"remove '{dbname}' result: {not os.path.exists(dbname)}")
    else:
        print(f"'{dbname}' doesn't exist. no cleanup needed.")
        return


def test_create_db(t_db: DB) -> None:
    assert isinstance(t_db, DB)


def test_create_table(t_db: DB) -> None:
    tbl_name = "test_create_table"
    t_def = {"col1": "TEXT", "col2": "INTEGER", "col3": "REAL"}
    e_data = [
        (0, "id", "INTEGER", 0, None, 1),
        (1, "col1", "TEXT", 0, None, 0),
        (2, "col2", "INTEGER", 0, None, 0),
        (3, "col3", "REAL", 0, None, 0),
    ]
    e_cols = ["id", "col1", "col2", "col3"]
    t_db.create_table(tbl_name, **t_def)
    tables = t_db.list_tables()
    assert tbl_name in tables

    cols = t_db.list_table_col_defs(tbl_name)
    assert cols == e_data

    colnames = t_db.list_table_cols(tbl_name)
    assert colnames == e_cols


def test_insert_full_record(t_db: DB) -> None:
    tbl_name = "test_insert_full_record"
    t_def = {"col1": "TEXT", "col2": "INTEGER", "col3": "REAL"}
    t_data = {"col1": "TEXT", "col2": 1, "col3": 1.234}
    e_data = [(1, "TEXT", 1, 1.234)]
    t_db.create_table(tbl_name, **t_def)
    t_db.insert_into(tbl_name, **t_data)
    result = t_db.execute(f"SELECT * from {tbl_name};")
    print(result)
    assert len(result) == 1
    assert result == e_data


def test_insert_part_record(t_db: DB) -> None:
    tbl_name = "test_insert_part_record"
    t_def = {"col1": "TEXT", "col2": "INTEGER", "col3": "REAL"}
    t_data_1 = {"col1": "TEXT"}
    t_data_2 = {"col2": 1, "col3": 1.234}
    t_data_3 = {"col3": 1.234}
    e_data = [(1, "TEXT", None, None), (2, None, 1, 1.234), (3, None, None, 1.234)]
    t_db.create_table(tbl_name, **t_def)
    t_db.insert_into(tbl_name, **t_data_1, close=False)
    t_db.insert_into(tbl_name, **t_data_2, close=False)
    t_db.insert_into(tbl_name, **t_data_3)
    result = t_db.execute(f"SELECT * from {tbl_name};")
    print("result:", result)
    assert len(result) == 3
    assert result == e_data
