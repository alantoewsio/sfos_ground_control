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

import streamlit as st
import pandas as pd
import time


# Function to parse log line
def parse_log_line(log_line) -> dict:
    """Extract date and severity from log entries

    Args:
        line (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        parts = log_line.split(" ", 2)
        log_timestamp = parts[0].strip('"')
        log_severity = parts[1].strip('"')
        log_contents = parts[2].strip()
        return {
            "timestamp": log_timestamp,
            "severity": log_severity,
            "message": log_contents,
        }
    except IndexError:
        return {"timestamp": None, "severity": None, "message": log_line}


# Function to read the last n lines of a file
def tail(file_path, n=100):
    """
    Reads the last n lines from a text file.

    :param file_path: Path to the text file.
    :param n: Number of lines to read from the end of the file.
    :return: A list containing the last n lines.
    """
    with open(file_path, "rb") as file:
        file.seek(0, 2)  # Move to the end of the file
        file_size = file.tell()
        buffer_size = 1024
        buffer = b""
        loglines = []

        while file_size > 0 and len(loglines) <= n:
            seek_position = max(file_size - buffer_size, 0)
            file.seek(seek_position)
            buffer = file.read(file_size - seek_position) + buffer

            # Split the buffer into lines but handle incomplete lines carefully
            loglines = buffer.splitlines()

            # If we have read enough lines, stop
            if len(loglines) > n:
                break

            # Update file size for the next chunk
            file_size = seek_position

    # To ensure we return exactly n lines, slice the list accordingly
    return [line.decode("utf-8") for line in loglines[-n:]]


# Function to continuously monitor log file
def monitor_log_file(log_file, dataframe: dict, n=100):
    """Watch a log file for changes

    Args:
        file_path (_type_): _description_
        dataframe (_type_): _description_
        n (int, optional): _description_. Defaults to 100.
    """
    with open(log_file, "r", encoding="utf-8") as file:
        file.seek(0, 2)  # Move pointer to end of file
        while True:
            log_line = file.readline()
            if log_line:
                dataframe.append(parse_log_line(log_line))
            else:
                time.sleep(1)
            st.rerun()


# Set up the Streamlit app
st.title("Log File Monitor")

# File path input
selected_log_path = st.text_input("Enter the log file path:", "./logs/application.log")

# Search functionality
search_text = st.text_input("Search logs (severity or contents):", "")


# Load last 100 lines on first page load
if "parsed_logs" not in st.session_state:
    parsed_logs = [parse_log_line(log) for log in tail(selected_log_path)]
    st.session_state["parsed_logs"] = parsed_logs

parsed_logs = st.session_state["parsed_logs"]
st.write(f"Logs: {len(parsed_logs)}")

log_data = pd.DataFrame(parsed_logs, columns=["timestamp", "severity", "message"])
show_data = None
# Filter based on search text
if search_text:
    filtered_data = log_data[
        log_data.apply(
            lambda row: search_text.lower() in row["severity"].lower()
            or search_text.lower() in row["contents"].lower(),
            axis=1,
        )
    ]
    show_data = filtered_data
else:
    show_data = log_data

st.dataframe(show_data, use_container_width=True, hide_index=True, height=400)
# Start monitoring the log file
st.write("Monitoring log file for new entries...")
monitor_log_file(selected_log_path, parsed_logs)
