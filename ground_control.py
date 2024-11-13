"""Test App
"""

from datetime import datetime as dt
import streamlit as st

TIME_FMT = r"%a %b %d, %Y - %I:%M %p %z"
now = dt.now()


st.set_page_config(layout="wide")

dashboard_pages = [
    st.Page(
        page="sfos/gui/views/dashboard.py",
        title="Firewalls",
        icon=":material/bar_chart:",
        default=True,
    )
]
manage_pages = [
    st.Page(
        page="sfos/gui/views/editor.py",
        title="Setup",
        icon=":material/settings:",
    ),
    # test_page = st.Page(
    #     page="sfos/gui/views/component_testing.py",
    #     title="Test",
    #     icon=":material/labs:",
    # )
]
info_pages = [
    st.Page(
        page="sfos/gui/views/about.py",
        title="About",
        icon=":material/info:",
    ),
    st.Page(
        page="sfos/gui/views/live_log_viewer.py",
        title="Logs",
        icon=":material/description:",
    ),
]
# --- Navigation Setup [without sections]

st.logo("sfos/gui/assets/gclogo_name.webp")
pg = st.navigation(
    {
        "Dashboard": dashboard_pages,
        "Manage": manage_pages,
        "info": info_pages,
    },
    position="sidebar",
)
st.sidebar.markdown(
    f"""
###### UPDATED
###### {now.strftime(TIME_FMT)}"""
)
pg.run()
