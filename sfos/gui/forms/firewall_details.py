"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

import sqlite3
import streamlit as st

# import pandas as pd

from sfos.gui.queries.query import run_query, load_query_from_file


@st.dialog("Firewall Details", width="large")
def show_firewall_details(
    serial_number: str, conn: sqlite3.Connection
):  # , connection: sqlite3.Connection):
    """Show firewall details popover

    Args:
        serial_number (str): _description_
        connection (sqlite3.Connection): _description_
    """
    # Load queries
    fw_query = load_query_from_file("firewall_info.sql")
    lic_query = load_query_from_file("firewall_license_info.sql")
    hist_query = load_query_from_file("firewall_history.sql")

    # Run queries and get tab data
    fw_details_row = run_query(
        fw_query, conn, params=[serial_number], index_cols=["Setting"]
    )
    fw_details = fw_details_row.transpose()
    lic_details = run_query(lic_query, conn, params=[serial_number])
    hist_details = run_query(hist_query, conn, params=[serial_number])

    # Define the tabs to show
    info_tab, subs_tab, settings_tab = st.tabs(["Info", "Subscriptions", "Settings"])
    st.header(f"Firewall {serial_number}")

    with info_tab:
        st.subheader("Details", divider=True)
        st.table(fw_details)

    with subs_tab:
        st.subheader("Subscriptions", divider=True)
        st.table(lic_details)

    with settings_tab:
        st.subheader("Connection Info", divider=True)
        st.write("Coming soon..")
        # edit_record()

    st.subheader("Event History", divider=True)
    with st.expander("Event History"):
        st.dataframe(hist_details, hide_index=True)

    # column_config = ({"serial_number": st.column_config.LinkColumn()},)
