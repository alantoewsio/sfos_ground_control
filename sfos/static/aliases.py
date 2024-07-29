from typing import Literal, TypeAlias


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
