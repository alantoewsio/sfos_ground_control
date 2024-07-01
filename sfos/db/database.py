# import csv
from datetime import datetime
import os
import sqlite3

from sqlite3 import Connection, Cursor
from typing import Any

from sfos.db.query import Select


class Database:
    def __init__(self, filename: str | None = None):
        self.filename = filename
        self.connection: Connection | None = None
        self.cursor: Cursor | None = None

    def get_connection(self, get_cursor: bool) -> tuple[Connection, Cursor | None]:
        try:
            if self.connection:
                self.cursor = self.cursor or self.connection.cursor()
                return self.connection, self.cursor
            self.connection = sqlite3.connect(
                self.filename,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            self.cursor = (
                self.cursor or self.connection.cursor() if get_cursor else None
            )
            return self.connection, self.cursor
        except Exception as e:
            raise e

    def close_connection(self, commit: bool = True) -> None:
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
            self.execute("CREATE TABLE IF NOT EXISTS version (version TEXT);")
            self.execute("INSERT INTO version (version) VALUES ('1.0');")
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
            column_defs = ", ".join(
                [f"{name} {cdef}" for name, cdef in columns.items()]
            )
            sql = (
                f"CREATE TABLE {table_name} "
                f"( id INTEGER PRIMARY KEY AUTOINCREMENT, {column_defs} )"
            )
            print(sql)
            cursor.execute(sql)

            if close:
                self.close_connection()
            return True
        except Exception as e:
            raise e

    def select(
        self,
        *columns: str,
        from_table: str,
        distinct: bool = False,
        limit: int | None = None,
    ) -> Select:
        return Select(
            *columns,
            from_table=from_table,
            distinct=distinct,
            limit=limit,
            _cursor=self.get_cursor,
            _execute=self.execute,
        )

    def load_query(self, filename: str) -> Select:
        return Select(
            from_file=filename, _execute=self.execute, _cursor=self.get_cursor
        )

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

    def _escape(self, value: str) -> str:
        value = value.replace("'", r"\'")
        value = value.replace("\\", r"\\")
        value = value.replace("\n", r"\n")
        value = value.replace("\r", r"\r")
        value = value.replace("\t", r"\t")
        value = value.replace("<", r"(")
        value = value.replace(">", r")")
        return value

    def _fmt(self, value: Any) -> str:
        if value == "?":
            return value
        if isinstance(value, str):
            return f"\"{self._escape(value)}\""
        if isinstance(value, int):
            return f"{value}"
        if isinstance(value, datetime):
            return str(value.timestamp())
        return str(value)

    def upsert(self, table: str, key_col: str, key_val: str, **field_data) -> list:
        all_cols = self.list_table_cols(table)
        update_cols = list(field_data.keys())
        params = list(field_data.values())
        # update_values = ["?"]*len(update_cols)

        keep_or_upd = []
        for col in all_cols:
            keep_or_upd.append(f"new.{col}" if col in update_cols else f"old.{col}")
        upsert_cols = ", ".join(keep_or_upd)
        upd_cols = ", ".join(update_cols)
        # upd_vals = ", ".join([self._fmt(value) for value in update_values])
        upd_vals = ", ".join([self._fmt(value) for value in params])  # update_values])
        sql = (
            f"WITH new ({upd_cols}) AS ( VALUES({upd_vals}) ) "
            f"INSERT OR REPLACE INTO {table} ({", ".join(all_cols)}) "
            f"SELECT {upsert_cols} "
            f"FROM new LEFT JOIN {table} AS old "
            f"ON new.{key_col} = old.{key_col} "
            # f"WHERE old.{key_col}='{key_val}' "
        )
        # try:
        # result = self.execute(sql, parameters=params, close=False)
        result = self.execute(sql,  close=False)
        return result
        # except Exception as e:
        #     print("Execute error: ", str(e), type(e))

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

    # def write_to_csv(results: list, filename: str) -> None:

    #     print("First Result:", results[0])
    #     raise NotImplementedError("csv writer not implemented")

    #     with open(filename, "w", newline="") as f:
    #         writer = csv.writer(f)

    #         writer.writerow(["Column 1", "Column 2", ...])
    #         for record in results:
    #             writer.writerows(record)

    def get_cursor(
        self,
        statement: str,
        parameters: list = [],
    ) -> Cursor:
        # try:
        conn, cursor = self.get_connection(get_cursor=True)
        cursor.execute(statement, parameters)

        return cursor
        # except Exception as e:
        #     raise e

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
