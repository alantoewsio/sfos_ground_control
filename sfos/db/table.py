from __future__ import annotations
from typing import Literal, TypeAlias

PrimaryKey: TypeAlias = Literal["PRIMARY KEY", "PRIMARY KEY AUTOINCREMENT"]
NotNull: TypeAlias = Literal["NOT NULL"]
Unique: TypeAlias = Literal["UNIQUE"]
Constraint: TypeAlias = PrimaryKey | NotNull | Unique | None


class Table:
    """Encapsulates the information necessary to represent a sqlite table"""

    def __init__(self, name: str, *columns: Column) -> None:
        self.name = name

        self._columns = list(columns)


class Column:

    def __init__(
        self,
        name: str,
        data_type: Literal[
            "TEXT", "INTEGER", "REAL", "BLOB", "TIMESTAMP", "DATE", "DATETIME", "NONE"
        ] = "TEXT",
        size: int = None,
        primary_key: bool = False,
        not_null: bool = False,
        unique: bool = False,
        default: str = None,
    ) -> None:
        self.name = name
        self.data_type = data_type
        self.size = size
        self.primary_key = primary_key
        self.not_null = not_null
        self.unique = unique
        self.default = default or ""

    def __sql__(self) -> str:
        data_type = f" {self.data_type}" if self.data_type else ""
        val = f"{self.name}{data_type},"
