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
from typing import Callable, TypeAlias
# from attr import dataclass
import streamlit as st

from sfos.static import exceptions as _ex
from sfos.gui.queries import run_query, load_query_from_file, PageData


PropValue: TypeAlias = str|int|bool|None

def _not_overridable(method: Callable):
    # Use as decorator to prevent a child class from ovverriding a method
    method.is_final = True # type:ignore
    return method

@st.dialog("Alert")
def show_alert_dialog(message: str):
    """Show a modal dialog with the title Alert

    Args:
        message (str): Message to show in dialog
    """
    st.write(message)

class Widget:
    """A base chart class"""

    def __init__(
        self,
        connection: Connection,
        title: str,
        *where_filters: str,
        query: str|None = None,
        query_file: str|None = None,
        **properties: PropValue,
    ):
        self.properties = dict(properties) or {}
        self._default_properties = {"height": 160, "paged": False, "page_size": 20}
        self.paged = self._get_property("paged", False)

        self.page_size = self._get_property("page_size", 20)
        row_ht = self._get_property("row_height", 35) # type:ignore
        self._default_properties["height"] = (self.page_size + 1) * row_ht # type:ignore

        self.connection = connection
        self.title = title
        self.query_file = query_file
        self.where_filters = where_filters
        self.query = load_query_from_file(query_file) if query_file else query

        # Streamlit element that can be clicked
        self.clicked = None
    def __filter__(self,*where_filters:str):
        self.where_filters=where_filters


    def __query__(self)->str:
        if not self.query:
            raise _ex.PropertyNotSetError("Query statement is not set")
        where_filters = (
            f"WHERE {" AND ".join(self.where_filters)}"
            if self.where_filters else ""
        )
        query = (
            self.query if not self.where_filters
            else f"SELECT * FROM ({self.query}) {where_filters}"
        )
        return query

    def _get_property(self, name: str, default: PropValue) -> PropValue:
        if self.properties:
            return self.properties.get(
                name, self._default_properties.get(name, default)
            )
        else:
            return default

    def _fetch_data(
            self,
            current_page: int  = 0,
            show_row: int =-1,
            page_size: int =-1,
    ) -> PageData:
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
        data = PageData(data=results, page_size=page_size)
        data.set_page(page_no=current_page, row_no=show_row)
        return data
    
    def alert(self,message:str):
        """Show an alert dialog"""
        show_alert_dialog(message)

    @_not_overridable
    def show(self):
        """Refresh the data from the given query
        and filter and display the data in a chart"""
        # Orchestrate the drawing of the widget
        outer_height = self._get_property("height", 150) + 120 # type:ignore

        if self._get_property("outer_container", True):
            with st.container(height=outer_height, border=False):
                self._show_widget_container()
        else:
            self._show_widget_container()

    def _show_widget_container(self):
        # Draw the widget title and container then call show_chard_contents
        st.markdown(f"##### {self.title}")
        with st.container(
            height=self._get_property("height", 150), # type:ignore
            border=self._get_property("border", True), # type:ignore
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
        data = self._fetch_data()

        st.dataframe(data.all_rows, hide_index=True, use_container_width=True)

    def reload_query_file(self, query_file: str |None = None):
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
