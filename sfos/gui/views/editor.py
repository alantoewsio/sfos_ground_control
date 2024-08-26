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

import os
import streamlit as st
import yaml


# Load YAML file
def load_yaml(file_path) -> list[dict]:
    """load contents of dict into a yaml file and return as list"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []
    else:
        return []


# Save YAML file
def save_yaml(data: list[dict], file_path: str):
    """Save dict to yaml file"""

    # Don't include keys with default values
    for fw in data:
        if not fw["hostname"]:
            assert "Valid Hostname" is False
        if "username" in fw and not fw["username"]:
            fw.pop("username")
        if "password" in fw and not fw["password"]:
            fw.pop("password")
        if "port" in fw and fw["port"] == 4444:
            fw.pop("port")
        if "verify-tls" in fw and fw["verify-tls"] is True:
            fw.pop("verify-tls")
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file)


# Function to edit a record
def edit_record(record: dict):
    """Edit a firewall inventory record

    Args:
        record (dict): _description_

    Returns:
        _type_: _description_
    """
    hostname = st.text_input(
        "Hostname",
        record.get("hostname", ""),
        key="hostname",
    )
    username = st.text_input("Username", record.get("username", ""), key="username")
    password = record.get("password", "")
    password = st.text_input(
        "Password", record.get("password", ""), key="password", type="password"
    )
    port = st.number_input(
        "Port", min_value=1, max_value=65535, value=record.get("port", 4444), key="port"
    )
    verify_tls = st.checkbox(
        "Verify TLS", value=record.get("verify-tls", True), key="verify-tls"
    )

    # Return the updated record
    return {
        "hostname": hostname,
        "username": username,
        "password": password,
        "port": port,
        "verify-tls": verify_tls,
    }


# Load existing YAML data
FILE_PATH = "firewalls.yaml"  # Replace with your file path
firewalls = load_yaml(FILE_PATH)

# Top section with title and firewall count
st.title("Firewall Inventory Management")
st.subheader(f"Firewall list: ({len(firewalls)} entries)")

# Layout with two columns
col1, col2 = st.columns(2)

# Left column: List of entries
with col1:
    firewall_names = [entry.get("hostname", "Unnamed") for entry in firewalls]
    selected_firewall = st.radio(
        "", ["Add Firewall"] + firewall_names, key="selected_firewall"
    )

# Right column: Edit the selected record
with col2:
    if selected_firewall == "Add Firewall":
        st.write("### Add New Firewall")
        edited_record = edit_record({})
    else:
        index = firewall_names.index(selected_firewall)
        st.write(f"### Edit Firewall: {selected_firewall}")
        edited_record = edit_record(firewalls[index])

    bcol1, bcol2, bcol3 = st.columns(3)
    # Buttons for Save, Cancel, and Delete

    with bcol1:
        if st.button("Cancel", type="secondary"):
            st.rerun()
    with bcol2:
        if st.button("Save", type="primary"):
            if selected_firewall == "Add Firewall":
                firewalls.append(edited_record)
            else:
                firewalls[index] = edited_record
            save_yaml(firewalls, FILE_PATH)
            st.success(f"Firewall '{edited_record['hostname']}' saved!")
            st.rerun()
    with bcol3:
        if selected_firewall != "Add Firewall" and st.button(
            "Delete", help="Delete this record"
        ):
            firewalls.pop(index)
            save_yaml(firewalls, FILE_PATH)
            st.success(f"Firewall '{selected_firewall}' deleted!")
            st.rerun()
