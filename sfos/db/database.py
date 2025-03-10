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

# pylint: disable=broad-exception-caught

from datetime import datetime
import os
from pathlib import Path
import sqlite3

from sqlite3 import Connection, Cursor
from typing import Any

from sfos.db.query import Select
from sfos.db.data_formatting import qs, rs
from sfos.static import exceptions as _ex
from sfos.logging import (
    Level,
    db_log as log,
    db_logtrace as logtrace,
    db_logdebug as logdebug,
    db_logerror as logerror,
    db_loginfo as loginfo,
)


class DBError(Exception):
    """General eErrors raisef by Database class"""


class Database:
    """Lightweight wrapper for working with sqlite database"""

    def __init__(self, filename: str | None = None, init_sql: str | list | None = None):
        self.filename = filename
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None
        logdebug(
            f"Database __init__('{filename}') {f'with {len(init_sql)} init scripts' if isinstance(init_sql, list) else ''}"
        )
        if init_sql:
            if isinstance(init_sql, str):
                count = 1
            else:
                count = len(init_sql)

            logdebug(f"Executing init_sql ({count} scripts)")

            self.execute(init_sql)
        else:
            logdebug("No init_sql to execute")

    def get_connection(self) -> Connection:
        """Get a Connection to the current database

        Raises:
            _ex.DatabaseError: If database connection fails

        Returns:
            Connection: Open connection to the current database
        """
        try:
            if self.connection:
                return self.connection
            if self.filename:
                self.connection = sqlite3.connect(
                    database=self.filename,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                )
                self.cursor = self.cursor or self.connection.cursor()
                return self.connection
            raise _ex.DatabaseError("Failed to get database connection")
        except Exception as e:
            raise _ex.DatabaseError("Failed to get database connection") from e

    def get_cursor(self) -> Cursor:
        """Returns an active Cursor to the current database

        Raises:
            _ex.DatabaseError: If a cursor cannot be obtained

        Returns:
            Cursor: Database cursor
        """
        if self.cursor:
            return self.cursor
        elif self.connection:
            return self.connection.cursor()
        try:
            self.connection = self.get_connection()
            self.cursor = self.get_connection().cursor()
        except _ex.DatabaseError as e:
            raise _ex.DatabaseError("Failed to get cursor") from e

        if self.cursor:
            return self.cursor
        raise _ex.DatabaseError("DB Cursor not available")

    def get_connection_and_cursor(self) -> tuple[Connection, Cursor]:
        """Get a connection and optionally a cursor instance for the database.

        Args:
            get_cursor (bool): returnvalue will contain a Cursor instance if true

        Raises:
            e: _description_

        Returns:
            tuple[Connection, Cursor | None]: _description_
        """
        try:
            if self.connection:
                self.cursor = self.cursor or self.connection.cursor()
                return self.connection, self.cursor
            if self.filename:
                self.connection = sqlite3.connect(
                    database=self.filename,
                    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                )
                self.cursor = self.cursor or self.connection.cursor()
                return self.connection, self.cursor
            raise _ex.DatabaseError("No database specified")

        except Exception as e:
            raise _ex.DatabaseError("Error getting a db connection") from e

    def close_connection(self, commit: bool = True) -> None:
        """_summary_

        Args:
            commit (bool, optional): _description_. Defaults to True.
        """
        self.close_cursor()

        if self.connection and commit:
            self.connection.commit()
        if self.connection:
            self.connection.close()
        self.connection = None

    def close_cursor(self) -> None:
        """_summary_"""
        if self.cursor:
            self.cursor.close()
            self.cursor = None

    def create_db(self, *init_sql: str):
        """Create

        Raises:
            e: _description_

        Returns:
            _type_: _description_
        """

        try:
            for sql in init_sql:
                self.execute(sql)
            self.close_connection()
        except Exception as e:
            log(Level.ERROR, type=str(type(e)), message=str(e))
        if self.filename and Path(self.filename).is_file():
            return False
        return True

    def select(
        self,
        *columns: str,
        from_table: str | None = None,
        distinct: bool = False,
        limit: int | None = None,
        from_file: str | None = None,
        raw_sql: str | None = None,
    ) -> Select:
        """_summary_

        Args:
            from_table (str): _description_
            distinct (bool, optional): _description_. Defaults to False.
            limit (int | None, optional): _description_. Defaults to None.

        Returns:
            Select: _description_
        """
        return Select(
            *columns,
            from_table=from_table,
            distinct=distinct,
            limit=limit,
            from_file=from_file,
            raw_sql=raw_sql,
            _cursor=self.get_cursor,
            _execute=self.execute,
        )

    def list_sql_files(self, path: str, ext: str = ".sql"):
        if not os.path.exists(path):
            raise _ex.PathNotFound(f"Path '{path}' not found")
        sql_files = [file for file in os.listdir(path) if file.endswith(ext)]
        return sql_files

    def load_sql_from_file(self, filename: str, path: str) -> str | None:
        """Retrieve the sql found in the given filename or return default if not found

        Args:
            filename (str): Filename of the sql file to load.

            path (str, optional): Location to look for the file.
                                  Defaults to "sfos/base/db/sql/".
            default (str, optional): If the sql file does not exist,
                                    'default' wil be returned.
                                     Defaults to None.

        Returns:
            str: contents of sql file
        """
        filename = filename if filename.endswith(".sql") else f"{filename}.sql"
        qfile = Path(filename)
        qfile = Path(path, filename) if not qfile.is_file() else qfile
        if qfile.is_file():
            result = qfile.read_text(encoding="utf-8")
        else:
            if not Path(path).is_dir():
                raise _ex.PathNotFound(f"Path '{path}' not found")
            raise _ex.FileNotFound(f"File '{qfile}' not found")

        logdebug(file=str(qfile), result=str(result))
        return result

    def load_query(self, filename: str) -> Select:
        """_summary_

        Args:
            filename (str): _description_

        Returns:
            Select: _description_
        """
        return Select(from_file=filename, _execute=self.execute, _cursor=self.get_cursor)

    def list_tables(self, close: bool = True) -> list:
        """_summary_

        Args:
            close (bool, optional): _description_. Defaults to True.

        Returns:
            list: _description_
        """
        cursor = self.get_cursor()
        if not cursor:
            return []
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()

        if close:
            self.close_connection()
        return [item for (item,) in result]

    def list_views(self, close: bool = True) -> list:
        """_summary_

        Args:
            close (bool, optional): _description_. Defaults to True.

        Returns:
            list: _description_
        """
        cursor = self.get_cursor()
        if not cursor:
            return []
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        result = cursor.fetchall()

        if close:
            self.close_connection()
        return [item for (item,) in result]

    def list_table_cols(self, table_name: str, close: bool = True) -> list:
        """_summary_

        Args:
            table_name (str): _description_
            close (bool, optional): _description_. Defaults to True.

        Returns:
            list: _description_
        """
        result = self.execute(f"PRAGMA table_info({table_name});")
        if close:
            self.close_connection()
        return [cols[1] for cols in result]

    def list_table_col_defs(self, table_name: str, close: bool = True) -> list:
        """_summary_

        Args:
            table_name (str): _description_
            close (bool, optional): _description_. Defaults to True.

        Returns:
            list: _description_
        """
        result = self.execute(f"PRAGMA table_info({table_name});")
        if close:
            self.close_connection()
        return result

    def insert_into(
        self,
        table_name: str,
        ignore_extra=False,
        close: bool = True,
        replace: bool = False,
        **field_data,
    ):
        """_summary_

        Args:
            table_name (str): _description_
            ignore_extra (bool, optional): _description_. Defaults to False.
            close (bool, optional): _description_. Defaults to True.
            replace (bool, optional): _description_. Defaults to False.

        Raises:
            Exception: _description_
            e: _description_

        Returns:
            _type_: _description_
        """
        try:
            cursor = self.get_cursor()
            if not cursor:
                return False

            columns = list(field_data.keys())
            values = list(field_data.values())

            if not ignore_extra:
                cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = {col[1]: col for col in cursor.fetchall()}
                for col in columns:
                    if col not in existing_columns:
                        raise DBError(
                            f"Column '{col}' does not exist in table '{table_name}'."
                        )

            placeholders = ", ".join("?" * len(columns))
            sql = (
                f"INSERT {'OR REPLACE' if replace else ''} "
                f"INTO {table_name} ({', '.join(columns)}) "
                f"VALUES ({placeholders})"
            )

            cursor.execute(sql, values)
            result = cursor.rowcount
            if close:
                self.close_connection()
            return result
        except Exception as e:
            raise e

    def get_cursor_for_statement(
        self,
        statement: str | None,
        parameters: list | None = None,
    ) -> Cursor:
        """Get a cursor instance for the database

        Args:
            statement (str): _description_
            parameters (list, optional): _description_. Defaults to None.

        Returns:
            Cursor: a cursor to work with the currnet db
        """
        # try:
        cursor = self.get_cursor()
        if not cursor:
            raise _ex.DatabaseError("Unable to obtain a cursor.")
        logtrace(statement=str(statement), parameters=str(parameters))
        if statement and parameters:
            cursor.execute(statement, parameters)

        return cursor
        # except Exception as e:
        #     raise e

    def execute(
        self,
        statements: str | list[str],
        close: bool = True,
        params: list | None = None,
    ) -> list[Any]:
        results = []
        if isinstance(statements, str):
            statements = [statements]

        for statement in statements:
            if Path(statement).is_file():
                loginfo(f"Executing SQL Script '{statement}'")
                statement = self.load_sql_from_file(statement)
            results.append(self._execute(statement, close, params))

        return results

    def _execute(
        self,
        statement: str,
        close: bool = True,
        params: list | None = None,
    ) -> list[Any]:
        """_summary_

        Args:
            statement (str): _description_
            close (bool, optional): _description_. Defaults to True.
            params (list, optional): _description_. Defaults to [].

        Raises:
            e: _description_

        Returns:
            _type_: _description_
        """
        try:
            cursor = self.get_cursor()
            if statement.count(";") > 1 and not params:
                logdebug(
                    "Using cursor.executescript",
                    separators=statement.count(";"),
                    params=params is not None,
                )
                execute = cursor.executescript
            else:
                logdebug("Using cursor.execute")
                execute = cursor.execute

            # Reworked to catch execution errors and to simplify logic
            try:
                args = [statement, params] if params else [statement]
                logtrace(
                    method=execute.__name__,
                    sql=statement,
                    params=params if params else str(None),
                )
                execute(*args)
                results = cursor.fetchall()
            except sqlite3.IntegrityError as e:
                logerror(e)
                print("Database operation error:", str(e), f"data={params}")
                results = []

            if close:
                self.close_connection()

            return results
        except sqlite3.OperationalError as e:
            logdebug(exception=f"{type(e)}:{str(e)}")

    def insert_or_update(
        self,
        insert_into: str,
        data: dict,
        on_conflict: list[str],
        increment: list[str] | None = None,
    ) -> bool:
        """Insert new records or update columns on existing records if colflict found"""
        # Remove columns listed in increment so they aren't duplicated
        if increment:
            for col in increment:
                data.pop(col, None)
            for col in increment:
                data[col] = 0
        else:
            increment = []

        cols = list(f"'{name}'" if " " in name else name for name in data.keys())
        column_names = ", ".join(cols)
        key_names = ", ".join([qs(name) for name in on_conflict])
        param_strs = ", ".join([f":{rs(name)}" for name in data.keys()])
        tmp_param_values = list(data.values())

        # Handle value formatting
        param_values = []
        for val in tmp_param_values:
            if val is None:
                param_values.append("NULL")
            elif isinstance(val, datetime):
                param_values.append(val.isoformat())
            else:
                param_values.append(val)

        updates = []
        for col in cols:
            updates.append(
                f"{col} = {insert_into}.{col} + 1"
                if col in increment
                else f"{col} = CASE WHEN excluded.{col} != {insert_into}.{col} "
                f"AND excluded.{col} IS NOT NULL "
                f"THEN excluded.{col} ELSE {insert_into}.{col} END"
            )
        sql = (
            f"INSERT INTO {insert_into} (\n     {column_names})\n"
            f"VALUES (\n     {param_strs})\n"
            f"ON CONFLICT ({key_names}) DO UPDATE SET\n"
            f"{',\n'.join(updates)};"
        )

        try:
            self.execute(sql, params=param_values)
            return True
        except sqlite3.ProgrammingError as e:
            logerror(
                "Error with statement. Has the database structure changed?",
                msg=str(e),
            )

        except sqlite3.OperationalError as e:
            logerror(
                "Error with statement. Has a table or query been renemaed?",
                msg=str(e),
            )

        return False
