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

from sqlite3 import Connection
from typing import Any
import streamlit as st
from sfos.gui.widgets.widget import Widget


class Metric(Widget):
    """A donut chart class"""

    def __init__(
        self,
        connection: Connection,
        title: str,
        *where_filters: str,
        query: str = None,
        query_file: str = None,
        **properties: str | int | bool,
    ):
        """_summary_

        Args:
            connection (Connection): _description_
            title (str, optional): _description_. Defaults to "Donut".
            query (str, optional): _description_. Defaults to None.
            query_file (str, optional): _description_. Defaults to None.
            properties (str | int | bool, optional): e.g. {"height": 150}

            Metric properties:
                font_size (str): Defaults to 5rem
        """
        super().__init__(
            connection,
            *where_filters,
            title=title,
            query=query,
            query_file=query_file,
            **properties,
        )

    def draw_contents(self):
        """Display the latest query data in donut chart"""

        data = self._fetch_data()[0]
        num = format_number(data["count"].iloc[0])
        sz = self._get_property("font_size", "5rem")
        st.html(
            f"<div align='center' style='font-weight: bold;font-size: {sz}'>{num}</div>"
        )

    def __call__(self) -> Any:
        return self.show()


def format_number(num: float | int) -> str:
    """Format a number im millions, thousands or less

    Args:
        num (float | int): Number to format

    Returns:
        str: Number string formatted in millions, thousands, or less
    """
    if num > 1000000:
        if not num % 1000000:
            return f"{num // 1000000} M"
        return f"{round(num / 1000000, 1)} M"
    if num > 1000:
        if not num % 1000:
            return f"{num // 1000} K"
        return f"{round(num / 1000, 1)} K"
    return f"{num}"
