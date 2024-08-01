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
    def __init__(
        self,
        *columns: str,
        from_table: str | None = None,
        distinct: bool = False,
        limit: int | None = None,
        _execute: Callable[[str, list], list] | None = None,
        _cursor: Cursor | None = None,
        from_dict: dict | None = None,
        from_file: str | None = None,
    ) -> None:
        self._table = self._save_columns = self._columns = None
        self._distinct = self._limit = self._execute = None
        self._where = self._order = self._group = self._params = []

        if from_file:
            from_dict = self._import(from_file)

        if from_dict:
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

    def _init_worker(
        self,
        columns: list[str] = [],
        from_table: str | None = None,
        distinct: bool = False,
        limit: int | None = None,
        where: list[_Where] = [],
        order: list[_OrderBy] = [],
        group: list[str] = [],
        _execute: Callable[[str, list], list] | None = None,
        _cursor: Cursor | None = None,
    ) -> None:
        if not from_table:
            raise ArgumentError("Missing argument 'from_table'")

        self._from = [FromTable(from_table)] if from_table else []
        self._save_columns = columns if columns else None
        self._columns = columns if columns else ["*"]  # [self._table + ".*"]
        self._distinct = distinct or False
        self._limit = limit
        self._where = [_Where(**item) for item in where]
        self._order = [_OrderBy(**item) for item in order]
        self._group = group
        self._params = []
        self._execute = _execute
        self._cursor = _cursor

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
        self._from.append(FromTable(table_name))
        return self

    def from_subquery(self, subquery: Select) -> Self:
        self._from.append(Subquery(subquery))
        return self

    def where(
        self,
        column: str,
        operator: QueryOperators = "Like",
        criteria: str | list[str] | None = None,
    ) -> Self:
        self._where.append(_Where(column, operator, criteria))
        return self

    def order_by(
        self, column: str, ascending: bool = True, nulls_first: bool | None = None
    ) -> Self:
        self._order.append(_OrderBy(column, ascending, nulls_first))
        return self

    def group_by(self, column: str) -> Self:
        self._group.append(column)
        return self

    def limit(self, count: int) -> Self:
        self.limit = count
        return self

    def fetchall(self) -> list | None:
        if self._execute:
            return self._execute(self.__sql__, parameters=self._params)
        print("No execute function to return")

    def get_cursor(self) -> Cursor | None:
        if self._cursor:
            return self._cursor(self.__sql__, parameters=self._params)
        print("No cursor to return")

    @property
    def __sql__(self) -> str:
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
        with open(filename, "w") as qfile:
            json.dump(self.__dict__, qfile, indent=indent)

    def _import(self, filename: str) -> dict:
        if isinstance(filename, list):
            filename = "".join(filename)
        with open(filename, "r") as qfile:
            return json.load(qfile)


class FromTable:
    def __init__(self, table: str):
        self.table = table

    def __sql__(self) -> str:
        return f"{self.table}"

    @property
    def __dict__(self) -> dict:
        return {"table": self.from_table}


class Subquery:
    def __init__(
        self,
        subquery: Select,
        as_name: str | None = None,
    ) -> None:
        self.as_name = as_name
        self.subquery = subquery

    @property
    def __sql__(self) -> str:
        asname = f" AS {self.as_name}" if self.as_name else ""
        return f"({self.subquery.__sql__}){asname}"

    @property
    def __dict__(self) -> dict:
        return {"table": self.from_table}


class _OrderBy:
    def __init__(
        self,
        column: str,
        ascending: bool | None = None,
        nulls_first: bool | None = None,
    ) -> None:
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
        return f"{self.column}{self.ascending}{self.nulls_first}"

    @property
    def __dict__(self) -> dict:
        return {
            "column": self.column,
            "ascending": self._ascending,
            "nulls_first": self._nulls_first,
        }


class FromJoin:

    def __init__(
        self,
        table_or_subquery: str | Subquery,
        operator: Literal["natural", "cross"] | None = None,
        join: Literal["left", "right", "full", "inner"] | None = None,
        outer: bool = False,
        on_expression: str | None = None,
        *using: str,
    ) -> None:
        self._table_or_subquery = table_or_subquery
        self._operator = operator
        self._join = join
        self._outer = outer
        self._on_expression = on_expression
        self._using = using
        if operator:
            assert on_expression is None
            assert not using
        if operator == "cross":
            assert not join

    @property
    def __sql__(self) -> str:
        sql += f"{self._operator.upper} " if self._operator else ""
        sql += "OUTER " if self._outer and self._join else ""
        sql += f"{self._join.upper} " if self._join else ""

        if isinstance(self._table_or_subquery, Subquery):
            sql += self._table_or_subquery.__sql__
        else:
            sql += self._table_or_subquery

        if self._on_expression:
            sql += f" ON {self._on_expression}"

        elif self._using:
            sql += f" USING ({', '.join(self._using)})"

        return f"{self.column}{self.ascending}{self.nulls_first}"

    @property
    def __dict__(self) -> dict:
        return {
            "column": self.column,
            "ascending": self._ascending,
            "nulls_first": self._nulls_first,
        }


class _Where:
    def __init__(
        self,
        column: str,
        operator: QueryOperators = "Like",
        criteria: str | None = None,
    ):

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
