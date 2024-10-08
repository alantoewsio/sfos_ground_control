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
import altair as alt

from sfos.gui.widgets.widget import Widget, PropValue


class Donut(Widget):
    """A donut chart class"""

    def __init__(
        self,
        connection: Connection,
        *where_filters: str,
        title: str = "Donut",
        query: str | None = None,
        query_file: str | None = None,
        **properties: PropValue,
    ):
        """_summary_

        Args:
            connection (Connection): _description_
            title (str, optional): _description_. Defaults to "Donut".
            query (str, optional): _description_. Defaults to None.
            query_file (str, optional): _description_. Defaults to None.
            properties (dict, optional): e.g. {"height": 150, "inner_radius": 40}. Defaults to None.
        """
        super().__init__(
            connection,
            *where_filters,
            title=title,
            query=query,
            query_file=query_file,
            **properties,
        )
        self._default_properties["inner_radius"] = (
            self.properties.get(
                "height",
                self._default_properties.get("height", 160),
            )
            / 4
        )  # type:ignore

    def draw_contents(self):
        """Display the latest query data in donut chart"""

        data = self._fetch_data()

        height = self._get_property("height", 160) - 20  # type: ignore

        inner_radius = self._get_property("inner_radius", height / 4)  # type: ignore

        chart = (
            alt.Chart(data.all_rows, height=height)  # type:ignore
            .mark_text()
            .mark_arc(
                innerRadius=self.properties.get("inner_radius", inner_radius),
            )
            .encode(
                theta=alt.Theta(field="count", type="quantitative"),  # type:ignore
                color=alt.Color(
                    field="status",  # type:ignore
                    type="nominal",  # type:ignore
                ),
            )
        )
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    def __call__(self) -> Any:
        return self.show()
