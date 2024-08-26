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

from datetime import datetime
from sqlite3 import Connection

# from typing import Any

import streamlit as st

import pandas as pd

from sfos.gui.widgets.widget import Widget
from sfos.gui.widgets.page_selector import (
    pagination_controls,
    page_size_selector,
    page_selection_status,
)


class Table(Widget):
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
            **properties (str | int | bool, optional): e.g. {"height": 150, "inner_radius": 40}.

            Table properties:
                page_size (int): Defaults to 20
                row_height (int): Defaults to 35 - Only used to set table height


        """
        properties["paged"] = True
        properties["outer_container"] = False
        properties["border"] = False
        properties["filter_button"] = False
        super().__init__(
            connection,
            *where_filters,
            title=title,
            query=query,
            query_file=query_file,
            **properties,
        )

    def _draw_top_actions(self, download_data: pd.DataFrame):
        with st.container(
            border=False,
            height=70,
        ):  # Tools
            lcol1, lcol2, mcol, rcol1, rcol2 = st.columns(
                [4, 1, 4, 1.5, 1.5],
                vertical_alignment="bottom",
            )

            with lcol1:
                st.text_input(
                    label="Search",
                    key="search",
                    placeholder="enter value to search for (not implemented yet)",
                )
            with lcol2:
                st.button("Search", use_container_width=True)
            with mcol:
                pass
            with rcol1:

                # timestamp = datetime.now().strftime("%c").replace(" ", "_")
                # filename = f"firewalls_{timestamp}.xlsx"
                # dlfile = download_data.to_excel(filename, engine="xlsxwriter")
                # st.download_button(
                #     label="Download Excel",
                #     data=dlfile,
                #     file_name=filename,
                #     mime="text/csv",
                #     key="download-xlsx",
                #     use_container_width=True,
                # )
                pass

            with rcol2:
                dlfile = download_data.to_csv()
                timestamp = datetime.now().strftime("%c").replace(" ", "_")
                filename = f"firewalls_{timestamp}.csv"
                st.download_button(
                    label="Download .csv",
                    data=dlfile,
                    file_name=filename,
                    mime="text/csv",
                    key="download-csv",
                    use_container_width=True,
                )

    def draw_contents(self):
        """Display the latest query data in donut chart"""

        if "current_page" not in st.session_state:
            st.session_state["current_page"] = 0
        if "page_size" not in st.session_state:
            st.session_state["page_size"] = 25

        current_page = st.session_state["current_page"]
        page_size = st.session_state["page_size"]
        row_height = self._get_property("row_height", 35)

        page_data, row_count, current_page, page_count, all_data = self._fetch_data(
            current_page=current_page,
            page_size=page_size,
        )

        self._draw_top_actions(all_data)
        height = (len(page_data) + 1) * row_height
        self.clicked = st.dataframe(
            page_data,
            use_container_width=True,
            selection_mode="single-row",
            hide_index=True,
            height=height,
        )
        # Pagination
        with st.container():
            lcol, mcol, rcol = st.columns([1, 3, 1])
            with lcol:
                page_selection_status(current_page, page_count, row_count)

            with mcol:
                pagination_controls(current_page, page_count, 3)

            with rcol:
                page_size_selector()
