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

import os
import sqlite3

from sqlite3 import Connection, Cursor
from typing import Literal, TypeAlias

QueryOperators: TypeAlias = Literal[
    ">", "<", "=", "==", ">=", "<=", "!=", "like", "not", "is"
]

QuerySources: TypeAlias = Literal[
    "fwinfo_latest",
    "fwinfo_missing",
    "fwinfo",
]


class GroundControlDB:
    def __init__(self, filename: str | None = None):
        if not filename:
            filename = os.getenv("GROUND_CONTROL_DB_KEY", "./ground_control.sqlite3")

        self.filename = filename
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None

    def get_connection(self, get_cursor: bool) -> tuple[Connection, Cursor | None]:
        try:
            if self.connection:
                self.cursor = self.cursor or self.connection.cursor()
                return self.connection, self.cursor
            self.connection = sqlite3.connect(self.filename)
            self.cursor = (
                self.cursor or self.connection.cursor() if get_cursor else None
            )
            return self.connection, self.cursor
        except Exception as e:
            raise e

    def close_connection(
        self,
        commit: bool = True,
    ) -> None:
        self.close_cursor()

        if self.connection and commit:
            self.connection.commit()
        if self.connection:
            self.connection.close()
        self.connection = None

    def close_cursor(self) -> None:
        if self.cursor:
            self.cursor.close()
            self.cursor = None

    def create_db(self):
        if os.path.exists(self.filename):
            return False

        try:
            # conn = self.get_connection(get_cursor=False)
            # self.create_table("version", "version TEXT")
            self.execute("CREATE TABLE IF NOT EXISTS version (version TEXT);")
            self.execute("INSERT INTO version (version) VALUES ('1.0');")
            # self.insert_into("version", version="1.0")
            self.close_connection()
            return True
        except Exception as e:
            raise e

    def create_table(
        self,
        table_name: str,
        drop_if_exist: bool = False,
        close: bool = True,
        **columns: str,
    ):
        try:
            conn, cursor = self.get_connection(get_cursor=True)

            # Drop table if it exists and recreate
            if drop_if_exist:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            column_defs = [f"{name} {cdef}" for name, cdef in columns.items()]
            cursor.execute(
                f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                f" {', '.join(column_defs)});"
            )

            if close:
                self.close_connection()
            return True
        except Exception as e:
            raise e

    def list_tables(self, close: bool = True) -> list:
        conn, cursor = self.get_connection(get_cursor=True)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()

        if close:
            self.close_connection()
        return [item for item, in result]

    def list_views(self, close: bool = True) -> list:
        conn, cursor = self.get_connection(get_cursor=True)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        result = cursor.fetchall()

        if close:
            self.close_connection()
        return [item for item, in result]

    def list_table_cols(self, table_name: str, close: bool = True) -> list:
        result = self.execute(f"PRAGMA table_info({table_name});")
        if close:
            self.close_connection()
        return [cols[1] for cols in result]

    def list_table_col_defs(self, table_name: str, close: bool = True) -> list:
        result = self.execute(f"PRAGMA table_info({table_name});")
        if close:
            self.close_connection()
        return result

    def query_db(
        self,
        field: str | None = None,
        operator: QueryOperators = "Like",
        value: str | list[str] | None = None,
        source: QuerySources = "fwinfo_latest",
    ) -> list:
        cols = self.list_table_cols(source)
        if field not in cols:
            raise Exception("Invalid search field")
        SQL = f"SELECT * from {source}"

        if field and value:
            SQL += f" WHERE {field} {operator} ?"

        if value and operator == "like" and "%" not in value and "_" not in value:
            value = f"%{value}%"
        return self.execute(SQL, parameters=[value])

    def insert_into(
        self,
        table_name: str,
        ignore_extra=False,
        close: bool = True,
        **field_data,
    ):
        try:
            conn, cursor = self.get_connection(get_cursor=True)
            columns = list(field_data.keys())
            values = list(field_data.values())

            if not ignore_extra:
                cursor.execute(f"PRAGMA table_info({table_name});")
                existing_columns = {col[1]: col for col in cursor.fetchall()}
                for col in columns:
                    if col not in existing_columns:
                        raise Exception(
                            f"Column '{col}' does not exist in table '{table_name}'."
                        )

            placeholders = ", ".join("?" * len(columns))
            sql = (
                f"INSERT INTO {table_name} ({', '.join(columns)}) "
                f"VALUES ({placeholders})"
            )

            cursor.execute(sql, values)
            result = cursor.rowcount
            if close:
                self.close_connection()
            return result
        except Exception as e:
            raise e

    def execute(
        self,
        statement: str,
        close: bool = True,
        parameters: list = [],
    ):
        try:
            conn, cursor = self.get_connection(get_cursor=True)
            cursor.execute(statement, parameters)
            results = cursor.fetchall()
            if close:
                self.close_connection()
            return results
        except Exception as e:
            raise e
