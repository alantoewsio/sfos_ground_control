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

from typing import Literal, TypeAlias

from sfos.db import Database

QueryOperators: TypeAlias = Literal[
    ">",
    "<",
    "=",
    "==",
    ">=",
    "<=",
    "!=",
    "like",
    "not",
    "not like",
    "is",
    "is not",
    "in",
    "not in",
]

QuerySources: TypeAlias = Literal[
    "fwinfo_latest",
    "fwinfo_missing",
    "fwinfo",
]


class GroundControlDB(Database):

    def __init__(self, filename: str | None = None):
        if not filename:
            filename = os.getenv("GROUND_CONTROL_DB_KEY", "./ground_control.sqlite3")
        super().__init__(filename)

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
