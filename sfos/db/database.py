# import csv
from datetime import datetime
import os
import sqlite3

from sqlite3 import Connection, Cursor
from typing import Any

from sfos.db.query import Select
from sfos.logging.logging import Level, log

DATE_FMT = "%Y-%m-%d"
DATE_TIME_FMT = "%Y-%m-%d %H:%M:%S"


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
            return f'"{self._escape(value)}"'
        if isinstance(value, int):
            return f"{value}"
        if isinstance(value, datetime):
            return f'"{value.strftime(DATE_TIME_FMT)}"'
        return str(value)

    def partial_update(
        self,
        table: str,
        key_col: str | list[str],
        **field_data,
    ) -> list:
        unchanged_cols = self.list_table_cols(table)
        updating_cols = list(field_data.keys())
        new_vals = []
        increment_cols = []
        increment_vals = []

        for col, val in field_data.items():
            if col in unchanged_cols:
                unchanged_cols.remove(col)
            if val is None:
                new_vals.append("NULL")
            elif val == "<INCREMENT>":
                updating_cols.remove(col)
                increment_cols.append(col)
                increment_vals.append(f"old.{col} + 1 as {col}")
            else:
                new_vals.append(self._fmt(val))

        # list all columns in the order that values will be defined
        insert_into_c = []
        insert_into_c.extend(unchanged_cols)
        insert_into_c.extend(updating_cols)
        insert_into_c.extend(increment_cols)

        # Set the column order that values will be set in the final update query
        neworold_vals = []
        neworold_vals.extend([f"old.{col}" for col in unchanged_cols])
        neworold_vals.extend([f"new.{col}" for col in updating_cols])
        neworold_vals.extend(increment_vals)

        sub_join_c = ", ".join(neworold_vals)
        with_c = ", ".join(updating_cols)
        with_v = ", ".join(new_vals)
        insert_c = ", ".join(insert_into_c)

        sql_with_c_v = f"WITH new ({with_c}) AS (VALUES({with_v})) "
        sql_insert_c = f"INSERT OR REPLACE INTO {table} ({insert_c}) "
        if isinstance(key_col, list):
            key_cols = "USING(" + ",".join(key_col) + ")"
        else:
            key_cols = f"USING({key_col})"

        sql_sub_insert_v = (
            f"SELECT {sub_join_c} " f"FROM new LEFT JOIN {table} AS old {key_cols}"
        )

        sql = f"{sql_with_c_v}{sql_insert_c}{sql_sub_insert_v}"
        # print("partial_update sql=\n", sql)
        result = self.execute(sql, close=False)
        return result

    def insert_into(
        self,
        table_name: str,
        ignore_extra=False,
        close: bool = True,
        replace: bool = False,
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
            log(
                Level.ERROR,
                Error=f"{e}",
                statement=statement,
                parameters=parameters,
            )
            raise e
