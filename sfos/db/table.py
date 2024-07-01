from __future__ import annotations
from typing import Literal, TypeAlias

PrimaryKey: TypeAlias = Literal["PRIMARY KEY", "PRIMARY KEY AUTOINCREMENT"]
NotNull: TypeAlias = Literal["NOT NULL"]
Unique: TypeAlias = Literal["UNIQUE"]
Constraint: TypeAlias = PrimaryKey | NotNull | Unique | None


class Table:
    def __init__(self, name: str, *columns: Column) -> None:
        self.name = name
        self._columns = list(columns)


class Column:
    def __init__(
        self,
        name: str,
        data_type: str,
        constraint: Constraint,
    ) -> None:
        self.name = name
        self.data_type = data_type
        self.constraint = constraint
