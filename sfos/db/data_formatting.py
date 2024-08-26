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
from datetime import datetime
from typing import Any


DATE_FMT = "%Y-%m-%d"
DATE_TIME_FMT = "%Y-%m-%d %H:%M:%S"


def sql_escape(value: str) -> str:
    """Escape characters that can be unsafe in an sql string value

    Args:
        value (str): value to be inserted into an sql statement

    Returns:
        str: value with dangerous characters escaped
    """
    value = value.replace("'", r"\'")
    value = value.replace("\\", r"\\")
    value = value.replace("\n", r"\n")
    value = value.replace("\r", r"\r")
    value = value.replace("\t", r"\t")
    value = value.replace("<", r"(")
    value = value.replace(">", r")")
    return value


def sql_format(value: Any) -> str:
    """Format selected values correctly to be safely included in sql statement

    Args:
        value (Any): value to be included in sql

    Returns:
        str: value formatted correctly if it is a handled type or the original value
        unchanged
    """
    if value == "?":
        return value
    if isinstance(value, str):
        return f'"{sql_escape(value)}"'
    if isinstance(value, int):
        return f"{value}"
    if isinstance(value, datetime):
        return f'"{value.strftime(DATE_TIME_FMT)}"'
    return str(value)


DQ = '""'
SQ = "''"


def is_quote_wrapped(value: str, dq: bool = True, sq: bool = True) -> bool:
    """Check if string is enclosed in quotes

    Args:
        value (str): _description_
        dq (bool, optional): If True, check if string is enclosed in "double quotes".
                             Defaults to True.
        sq (bool, optional): If True, check if string is enclosed in 'single quotes'.
                             Defaults to True.

    Returns:
        bool: _description_
    """
    closures = [DQ, SQ] if dq and sq else [DQ] if dq else [SQ] if sq else []
    return is_enclosed(value, closures)


def is_enclosed(value, closures: list[str] | None = None) -> bool:
    """Check if string is enclosed in wrapping characters.

    Args:
        value (_type_): Value to check
        closures (list[str] | None, optional):A list of strings with encosing character
                        pairs.
                        Defaults to ["''", '""', "()", "[]", "{}", "<>"] if None

    Returns (bool):
        True - If the first and last chars in ANY closure string match the first
              and last characters in value.
        False - If no matches found.
    """
    closures = closures or ["''", '""', "()", "[]", "{}", "<>"]
    if not value or len(value) < 2:
        return False

    return f"{value[0]}{value[-1]}" in closures


def quote_wrap(value: str):
    """Ensure strings are quoted for sql otherwise leave it untouched

    Args:
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    if isinstance(value, str) and not is_quote_wrapped(value):
        return f"'{value}'"
    return value


def qs(value: str) -> str:
    """Quote a string if it contains a space"""
    return quote_wrap(value) if " " in value else value


def rs(value: str) -> str:
    """Replace spaces with underscores"""
    return value.replace(" ", "_") if " " in value else value
