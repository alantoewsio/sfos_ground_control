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

# pylint: disable=broad-exception-caught

from __future__ import annotations
import json
from sqlite3 import Cursor
from typing import Callable, Literal, Self, TypeAlias

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


class ArgumentError(Exception):
    """Raised when an invalid argument combination is given"""


class Select:
    """_summary_"""

    def __init__(
        self,
        *columns: str,
        from_table: str | None = None,
        distinct: bool = False,
        limit: int | None = None,
        _execute: Callable | None = None,
        _cursor: Callable | None = None,
        from_dict: dict | None = None,
        from_file: str | None = None,
        raw_sql: str | None = None,
    ) -> None:
        """_summary_

        Args:
            from_table (str | None, optional): _description_. Defaults to None.
            distinct (bool, optional): _description_. Defaults to False.
            limit (int | None, optional): _description_. Defaults to None.
            _execute (Callable[[str, list], bool, list] | None, optional): _description_. Defaults to None.
            _cursor (Cursor | None, optional): _description_. Defaults to None.
            from_dict (dict | None, optional): _description_. Defaults to None.
            from_file (str | None, optional): _description_. Defaults to None.
            raw_sql (str | None, optional): _description_. Defaults to None.
        """
        self._table = self._save_columns = self._columns = None
        self._distinct = self._limit = self._execute = None
        self._where = self._order = self._group = self._params = []

        if from_file:
            from_dict = self._import(from_file)
            if isinstance(from_dict, str):
                raw_sql = from_dict
                from_dict = None

        self.raw_sql = raw_sql
        if raw_sql:
            self._init_worker_base(_execute, _cursor)

        elif from_dict:
            if _execute and "_execute" not in from_dict:
                from_dict["_execute"] = _execute
            if _cursor and "_cursor" not in from_dict:
                from_dict["_cursor"] = _cursor
            self._init_worker(**from_dict)

        else:
            self._init_worker(
                columns=list(columns),
                from_table=from_table,
                distinct=distinct,
                limit=limit,
                _execute=_execute,
                _cursor=_cursor,
            )

    def _init_worker_base(
        self,
        _execute: Callable[[str, list], list] | None = None,
        _cursor: Cursor | None = None,
    ) -> None:
        """_summary_

        Args:
            _execute (Callable[[str, list], list] | None, optional): _description_. Defaults to None.
            _cursor (Cursor | None, optional): _description_. Defaults to None.
        """
        self._execute = _execute
        self._cursor = _cursor

    def _init_worker(
        self,
        columns: list[str] = None,
        from_table: str | None = None,
        distinct: bool = False,
        limit: int | None = None,
        where: list[_Where] = None,
        order: list[_OrderBy] = None,
        group: list[str] = None,
        _execute: Callable[[str, list], list] | None = None,
        _cursor: Cursor | None = None,
    ) -> None:
        """_summary_

        Args:
            columns (list[str], optional): _description_. Defaults to [].
            from_table (str | None, optional): _description_. Defaults to None.
            distinct (bool, optional): _description_. Defaults to False.
            limit (int | None, optional): _description_. Defaults to None.
            where (list[_Where], optional): _description_. Defaults to [].
            order (list[_OrderBy], optional): _description_. Defaults to [].
            group (list[str], optional): _description_. Defaults to [].
            _execute (Callable[[str, list], list] | None, optional):
                     _description_. Defaults to None.
            _cursor (Cursor | None, optional): _description_. Defaults to None.

        Raises:
            ArgumentError: _description_
        """
        if not from_table:
            raise ArgumentError("Missing argument 'from_table'")

        self._from = [FromTable(from_table)] if from_table else []
        self._save_columns = columns if columns else None
        self._columns = columns if columns else ["*"]  # [self._table + ".*"]
        self._distinct = distinct or False
        self._limit = limit
        self._where = [_Where(**item) for item in where] if where else []
        self._order = [_OrderBy(**item) for item in order] if order else []
        self._group = group if group else []
        self._params = []
        self._init_worker_base(_execute, _cursor)

    @property
    def __dict__(self) -> dict:
        return {
            "columns": self._save_columns,
            "from_table": self._table,
            "distinct": self._distinct,
            "where": [item.__dict__ for item in self._where],
            "order": [item.__dict__ for item in self._order],
            "group": self._group,
            "limit": self._limit,
        }

    def from_table(self, table_name: str) -> Self:
        """_summary_

        Args:
            table_name (str): _description_

        Returns:
            Self: _description_
        """
        self._from.append(FromTable(table_name))
        return self

    # def from_subquery(self, subquery: Select) -> Self:
    #     self._from.append(Subquery(subquery))
    #     return self

    def where(
        self,
        column: str,
        operator: QueryOperators = "Like",
        criteria: str | list[str] | None = None,
    ) -> Self:
        """_summary_

        Args:
            column (str): _description_
            operator (QueryOperators, optional): _description_. Defaults to "Like".
            criteria (str | list[str] | None, optional): _description_. Defaults to None.

        Returns:
            Self: _description_
        """
        self._where.append(_Where(column, operator, criteria))
        return self

    def order_by(
        self, column: str, ascending: bool = True, nulls_first: bool | None = None
    ) -> Self:
        """_summary_

        Args:
            column (str): _description_
            ascending (bool, optional): _description_. Defaults to True.
            nulls_first (bool | None, optional): _description_. Defaults to None.

        Returns:
            Self: _description_
        """
        self._order.append(_OrderBy(column, ascending, nulls_first))
        return self

    def group_by(self, column: str) -> Self:
        """_summary_

        Args:
            column (str): _description_

        Returns:
            Self: _description_
        """
        self._group.append(column)
        return self

    # def limit(self, count: int) -> Self:
    #     """_summary_

    #     Args:
    #         count (int): _description_

    #     Returns:
    #         Self: _description_
    #     """
    #     self.limit = count
    #     return self

    def fetchall(self) -> list | None:
        """_summary_

        Returns:
            list | None: _description_
        """
        if self._execute:
            return self._execute(self.__sql__, parameters=self._params)
        print("No execute function to return")

    def get_cursor(self) -> Cursor | None:
        """_summary_

        Returns:
            Cursor | None: _description_
        """
        if self._cursor:
            return self._cursor(self.__sql__, parameters=self._params)
        print("No cursor to return")

    @property
    def __sql__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        if self.raw_sql:
            return self.raw_sql

        _select = f"SELECT {", ".join(self._columns)} FROM {self._table}"

        _where = (
            " WHERE " + " AND ".join([this.__sql__ for this in self._where])
            if self._where
            else ""
        )
        params = (
            [this.__param__ for this in self._where if this.__param__]
            if self._where
            else []
        )
        self._params = params  # if params else None

        _group = " GROUP BY " + ", ".join(self._group) if self._group else ""
        _order = (
            " ORDER BY " + ", ".join([this.__sql__ for this in self._order])
            if self._order
            else ""
        )
        _limit = f" LIMIT {self._limit}" if self._limit else ""

        return f"{_select}{_where}{_group}{_order}{_limit}"

    def export(self, filename: str, indent=0) -> None:
        """_summary_

        Args:
            filename (str): _description_
            indent (int, optional): _description_. Defaults to 0.
        """
        with open(filename, "w", encoding="utf-8") as qfile:
            json.dump(self.__dict__, qfile, indent=indent)

    def _import(self, filename: str) -> dict | str:
        """_summary_

        Args:
            filename (str): _description_

        Returns:
            dict | str: _description_
        """
        if isinstance(filename, list):
            filename = "".join(filename)
        with open(filename, "r", encoding="utf-8") as qfile:
            try:
                return json.load(qfile)
            except Exception:
                return qfile


class FromTable:
    """_summary_"""

    def __init__(self, table: str):
        self.table = table

    def __sql__(self) -> str:
        return f"{self.table}"

    @property
    def __dict__(self) -> dict:
        return {"table": self.table}


# class Subquery:
#     def __init__(
#         self,
#         subquery: Select,
#         as_name: str | None = None,
#     ) -> None:
#         self.as_name = as_name
#         self.subquery = subquery

#     @property
#     def __sql__(self) -> str:
#         asname = f" AS {self.as_name}" if self.as_name else ""
#         return f"({self.subquery.__sql__}){asname}"

#     @property
#     def __dict__(self) -> dict:
#         return {"table": self.from_table}


class _OrderBy:
    """_summary_"""

    def __init__(
        self,
        column: str,
        ascending: bool | None = None,
        nulls_first: bool | None = None,
    ) -> None:
        """_summary_

        Args:
            column (str): _description_
            ascending (bool | None, optional): _description_. Defaults to None.
            nulls_first (bool | None, optional): _description_. Defaults to None.
        """
        self.column = column
        self._ascending = ascending
        self._nulls_first = nulls_first
        self.ascending = "" if ascending is None else " ASC" if ascending else " DESC"
        self.nulls_first = (
            ""
            if nulls_first is None
            else " NULLS FIRST" if nulls_first else " NULLS LAST"
        )

    @property
    def __sql__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"{self.column}{self.ascending}{self.nulls_first}"

    @property
    def __dict__(self) -> dict:
        """_summary_

        Returns:
            dict: _description_
        """
        return {
            "column": self.column,
            "ascending": self._ascending,
            "nulls_first": self._nulls_first,
        }


# class FromJoin:
#     """_summary_
#     """


#     def __init__(
#         self: Self@FromJoin,
#         table_or_subquery: str | Subquery,
#         operator: Literal["natural", "cross"] | None = None,
#         join: Literal["left", "right", "full", "inner"] | None = None,
#         outer: bool = False,
#         on_expression: str | None = None,
#         *using: str,
#     ) -> None:
#         self._table_or_subquery = table_or_subquery
#         self._operator = operator
#         self._join = join
#         self._outer = outer
#         self._on_expression = on_expression
#         self._using = using
#         if operator:
#             assert on_expression is None
#             assert not using
#         if operator == "cross":
#             assert not join

#     @property
#     def __sql__(self) -> str:
#         pass

#     @property
#     def __dict__(self) -> dict:
#         return {}


class _Where:
    def __init__(
        self,
        column: str,
        operator: QueryOperators = "Like",
        criteria: str | None = None,
    ):
        """_summary_

        Args:
            column (str): _description_
            operator (QueryOperators, optional): _description_. Defaults to "Like".
            criteria (str | None, optional): _description_. Defaults to None.
        """
        self._column = column
        self._operator = operator
        self._criteria = criteria

    @property
    def __dict__(self) -> dict:
        return {
            "column": self._column,
            "operator": self._operator,
            "criteria": self._criteria,
        }

    @property
    def __sql__(self) -> str:
        return f"{self._column} {self._operator} ?"

    @property
    def __param__(self) -> str:
        # If the user specified a 'lile' query but didn't
        # use wildcards then search for the criteria anywnere in the field
        if not self._criteria:
            self._criteria = "NULL"

        if (
            self._operator in ["like", "not like"]
            and "%" not in self._criteria
            and "_" not in self._criteria
        ):
            return f"%{self._criteria}%"

        return str(self._criteria)
