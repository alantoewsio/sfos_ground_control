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

from pathlib import Path
import streamlit as st
from sfos.gui.forms.contact import contact_form

ENCODING = "utf-8"
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("sfos/gui/assets/gclogo_lg.webp", width=300)


with col2:
    st.title("Ground Control", anchor=False)
    st.write("Ground Control is an onsite monitoring tool for SFOS Firewalls.")
    if st.button("📨 Report an issue"):
        contact_form()

st.write("\n")
st.subheader("Main Features", anchor=False)
st.write(
    """
    - Firewall inventory
    - Collect key firewall information - mode, serial number, licensed features and expiry
    - Monitor firewall online status
    """
)
st.write("\n")

lic_file = Path("./LICENSE")
if lic_file.exists():
    text = lic_file.read_text(ENCODING)
    st.text_area("License", text, height=600)
