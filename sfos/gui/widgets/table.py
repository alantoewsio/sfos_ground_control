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
from st_mui_table import st_mui_table as MuiTable

from sfos.gui.queries import PageData
from sfos.gui.widgets.widget import Widget


class Table(Widget):
    """A donut chart class"""

    def __init__(
        self,
        connection: Connection,
        title: str,
        *where_filters: str,
        query: str | None = None,
        query_file: str | None = None,
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
        self.refresh_data()

    def refresh_data(self):
        """Query latest date from db"""
        self.data = self._fetch_data()

    def _draw_top_actions(self, data: PageData):
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
                page_sizes = [0, 1, 5, 10, 25, 50, 100, 250, 500, 1000]

                st.select_slider(
                    label="Page Size",
                    key="set_page_size",
                    options=page_sizes,
                    value=self.data.page_size,
                )

            with rcol2:
                dlfile = data.all_rows.to_csv()
                timestamp = datetime.now().strftime(format="%c").replace(" ", "_")
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
        state = st.session_state

        if "where_filter" in state:
            self.__filter__(state["where_filter"])
        else:
            self.__filter__()
        self.refresh_data()

        # check if page size changed
        state["page_size"] = state.get("set_page_size", state.get("page_size", 5))
        state["current_page"] = (
            state.get("goto_page", state.get("current_page", 0) + 1) - 1
        )
        self.data.set_page_size(state["page_size"])
        self.data.set_page(page_no=state["current_page"])
        # self._draw_top_actions(data=self.data)

        # Draw the table
        state["table_height"] = (self.data.row_count + 1) * int(
            state.get("row_height", 35)
        )
        # https://pypi.org/project/st-mui-table/
        MuiTable(
            self.data.all_rows,
            enablePagination=True,
            customCss="",
            paginationSizes=[5, 10, 25, 50, 100, 250, 500, 1000],
            size="medium",
            padding="normal",
            showHeaders=True,
            key="mui_table",
            stickyHeader=True,
            paperStyle={
                "width": "100%",
                "overflow": "hidden",
                "paddingBottom": "1px",
                "border": "2px solid rgba(224, 224, 224, 1)",
            },
            detailColumns=[
                "model",
                "version",
                "company",
                "next_license_expiring",
                "expiry_date",
            ],
            detailColNum=2,
            detailsHeader="Firewall Details",
            showIndex=False,
        )
