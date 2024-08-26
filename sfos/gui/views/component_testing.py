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
import json
import sqlite3
import subprocess
import psutil
import streamlit as st

from streamlit_pills import pills
from streamlit_autorefresh import st_autorefresh

from sfos.gui.widgets import Donut, Metric, Table
from sfos.gui.forms.firewall_details import show_firewall_details

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
if "auto_refresh" not in st.session_state:
    st.session_state["auto_refresh"] = True

if "auto_refresh" in st.session_state and st.session_state["auto_refresh"]:
    st_autorefresh(interval=2000, key="dashboard_counter")


# The function returns a counter for number of refreshes. This allows the
# ability to make special requests at different intervals based on the count

# Connect to the SQLite database
conn = sqlite3.connect("ground_control.sqlite3", check_same_thread=False)
# Load widget definitions
widget_defs = json.load(open("sfos/gui/views/dashboard_widgets.json", encoding="utf-8"))


def _check_firewalls():
    st.session_state["check_start_time"] = datetime.now()
    nfo = subprocess.Popen(["python", "./sccli.py", "-i", "./firewalls.yaml"])
    st.session_state["check_pid"] = nfo.pid
    st.info(f"Started check ({nfo.pid}")
    # st.rerun()


# Start drawing the page
colL, colM, colR = st.columns([4, 1, 1])
with colL:
    st.title("Ground Control - Firewalls")
with colM:
    st.toggle("Auto Refresh", key="auto_refresh")
with colR:
    if "check_pid" in st.session_state:
        proc = psutil.Process(st.session_state["check_pid"])
        if not proc.status == "running":
            st.info(f"process {st.session_state["check_pid"]} stopped")
            del st.session_state["check_pid"]
            del st.session_state["check_start_time"]
        else:
            diff = datetime.now() - st.session_state["check_start_time"]
            st.write(f"Running for {diff.total_seconds()}s")
    else:
        st.button(
            "Check",
            on_click=_check_firewalls,
        )

# Create the top-of-page widgets from defs
widgets = []
for w in widget_defs:
    match w["type"]:
        case "Metric":
            widgets.append(
                Metric(conn, query_file=w["q"], title=w["title"], **w["properties"])
            )
        case "Donut":
            widgets.append(
                Donut(conn, query_file=w["q"], title=w["title"], **w["properties"])
            )

# Now draw them on the page in an open expander
with st.expander(label="Firewall Status Summary", expanded=True):
    cols = st.columns(5)
    INDEX = 0
    for w in widgets:
        with cols[INDEX % 5]:
            w.show()
        INDEX += 1

# Check if any filters were clicked
if "where_filters" not in st.session_state:
    st.session_state["where_filters"] = []
where_filters = st.session_state["where_filters"]
# clear_clicked = None
for w in widgets:
    if w.clicked:
        for wdef in widget_defs:
            if wdef["title"] == w.title:
                st.write(wdef)
                st.session_state["where_filters"] = wdef["filter"]["filters"]
                pills("Showing:", [wdef["filter"]["name"]], ["🏷️"])

# Create the main table
fw_table = Table(
    connection=conn,
    query_file="dashboard.sql",
    where_filters=st.session_state["where_filters"],
    title="Managed Firewalls",
)

fw_table.show()

st.markdown("""---""")
# st.write(f"Refresh Counter: {count}")
# st.balloons()
# st.snow()
# # st.error("Error message")
# st.warning("Warning message")
# st.info("Info message")
# st.success("Success message")
# st.exception(Exception("Testing"))
