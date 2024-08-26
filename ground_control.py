"""Test App
"""

from datetime import datetime as dt
import streamlit as st

TIME_FMT = r"%a %b %d, %Y - %I:%M %p %z"
now = dt.now()


st.set_page_config(layout="wide")

dashboard_page = st.Page(
    page="sfos/gui/views/dashboard.py",
    title="Firewalls",
    icon=":material/bar_chart:",
    default=True,
)
setup_page = st.Page(
    page="sfos/gui/views/editor.py",
    title="Setup",
    icon=":material/settings:",
)
about_page = st.Page(
    page="sfos/gui/views/about.py",
    title="About",
    icon=":material/info:",
)
test_page = st.Page(
    page="sfos/gui/views/component_testing.py",
    title="Test",
    icon=":material/labs:",
)
log_page = st.Page(
    page="sfos/gui/views/live_log_viewer.py",
    title="Logs",
    icon=":material/description:",
)
# --- Navigation Setup [without sections]

st.logo("sfos/gui/assets/gclogo_name.webp")
pg = st.navigation(
    {
        "Dashboard": [dashboard_page],
        "Manage": [setup_page, test_page],
        "info": [about_page, log_page],
    },
    position="sidebar",
)
st.sidebar.markdown(
    f"""
###### UPDATED
###### {now.strftime(TIME_FMT)}"""
)
pg.run()
