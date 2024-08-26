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
from typing import Callable
import streamlit as st
import pandas as pd

from sfos.gui.queries.query import run_query, load_query_from_file


def _not_overridable(method: Callable):
    method.is_final = True
    return method


class Widget:
    """A base chart class"""

    def __init__(
        self,
        connection: Connection,
        title: str,
        *where_filters: str,
        query: str = None,
        query_file: str = None,
        **properties: str | int | bool,
    ):
        self.properties = dict(properties) or {}
        self._default_properties = {"height": 160, "paged": False, "page_size": 20}
        self.paged = self._get_property("paged", False)

        if self.paged:
            self.page_size = self._get_property("page_size", 20)
            self._default_properties["height"] = self.page_size * (
                self._get_property("row_height", 35) + 1
            )

        self.connection = connection
        self.title = title
        self.query_file = query_file
        self.where_filters = where_filters
        self.query = load_query_from_file(query_file) if query_file else query

        # Streamlit element that can be clicked
        self.clicked = None
    
    def __query__(self)->str:
        where_filters = (
            f"WHERE {" AND ".join(self.where_filters)}"
            if self.where_filters else ""
        )
        query = (
            self.query if not self.where_filters
            else f"SELECT * FROM ({self.query}) {where_filters}"
        )
        return query
    
    def _get_property(self, name: str, default: str | int = None) -> str | int:
        if self.properties:
            return self.properties.get(
                name, self._default_properties.get(name, default)
            )
        else:
            return default

    def _fetch_data(self, current_page:int = None, first_record:int = None, page_size:int = None) -> tuple[pd.DataFrame,int,int,int,int,pd.DataFrame]:
        """Return the selected page of data from the database

        Args:
            current_page (int, optional): Page number (first page=0). Defaults to None.
                                          If first_record and current_page are None, all records will be.
            first_record (int, optional): Set the page number to the page containing this record (first record=0). Defaults to None.
                                          If first_record and current_page are None, all records will be.
            page_size (int, optional): Number of records to include on a page. Defaults to None.
                                          If None, all data is returned

        Returns:
            tuple[pd.DataFrame,row_count:int,current_page:int,pages:int]: _description_
        """
        query = self.__query__()
        results =  run_query(query, self.connection)
        row_count = len(results)

        # early exit if no pagination needed
        if current_page is None and first_record is None:
            return (results,row_count,-1,-1,-1)


        #calculate how many pages are available
        (full_pages,remaining_rows) = divmod(row_count, page_size)
        page_count = full_pages + (1 if remaining_rows else 0)


        #Calculate which page to return:
        if first_record and first_record<0:
            # first_record takes precedence over page_number 
            current_page=0  # Set current_page to the first page

        elif first_record and first_record>row_count:
            current_page = page_count -1

        elif first_record:
            # Find the page of the requested first_record
            current_page=divmod(first_record, page_size)[0] 

        elif current_page and current_page < 0:
            current_page=0  # Set curreht_page to the first page

        elif current_page>=page_count:
            current_page= page_count-1 #set current_page to the last page

        # else: current_page is between 0 and pages - 1

        # Now find the first record on the chosen page
        first_record= page_size*current_page
        page_data=results[first_record:page_size]

        return (
            page_data,
            row_count,
            current_page,
            page_count,
            results,
        )



    @_not_overridable
    def show(self):
        """Refresh the data from the given query
        and filter and display the data in a chart"""
        # Orchestrate the drawing of the widget
        outer_height = self._get_property("height", 150) + 120

        if self._get_property("outer_container", True):
            with st.container(height=outer_height, border=False):
                self._show_widget_container()
        else:
            self._show_widget_container()

    def _show_widget_container(self):
        # Draw the widget title and container then call show_chard_contents
        st.markdown(f"##### {self.title}")
        with st.container(
            height=self._get_property("height", 150),
            border=self._get_property("border", True),
        ):
            self.draw_contents()

        if self._get_property("filter_button", True):
            self.clicked = st.button(
                "Filter",
                key=self.title,
                type="secondary",
                use_container_width=True,
            )

    def draw_contents(self):
        """Display the contents of the chart control"""
        st.dataframe(self._fetch_data(), hide_index=True, use_container_width=True)

    def reload_query_file(self, query_file: str = None):
        """Reload the query from file

        Args:
            query_file (str, optional): Overrides self.query_file if provided.
            Uses current self.query_file if None.
            No changes made if self.query_file is None and query_file is None
        """
        if query_file:
            self.query_file = query_file

        if self.query_file:
            self.query = load_query_from_file(self.query_file)
