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
import re
from datetime import datetime
import streamlit as st
import pandas as pd


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


def parse_log_line(line):
    """
    Parses a single log line into a dictionary.

    :param line:    A single log line as a string.
    :return:        A dictionary with parsed values or None if the line does not match
                    the expected format.
    """
    # Regular expression pattern to match the expected log format
    log_pattern = re.compile(
        r'(?P<datetime>\S+)\s+"(?P<log_level>\w+)"\s+(?P<key_values>.+)'
    )

    match = log_pattern.match(line)
    if not match:
        return None

    log_dict = {}

    # Parse the datetime and log level
    log_dict["timestamp"] = datetime.strptime(
        match.group("datetime"), "%Y-%m-%dT%H:%M:%SZ"
    )
    log_dict["log_level"] = match.group("log_level")

    # Parse the key-value pairs
    key_values = match.group("key_values").split()
    for kv in key_values:

        sp = kv.split("=", 1)
        print("split", type(kv), kv, type(sp), sp)
        if len(sp) == 1:
            sp.append(None)
        (key, value) = sp

        log_dict[key.strip()] = value.strip('"') if value else value

    return log_dict


def parse_log_lines(loglines: list[str]):
    """
    Parses a log file line by line into a list of dictionaries.

    :param file_path: Path to the log file.
    :return: A list of dictionaries, each representing a parsed log line.
    """
    keys_found = []
    parsed_logs = []
    for line in loglines:
        parsed_line = parse_log_line(line.strip())

        if parsed_line:
            keys_found.extend(parsed_line.keys())
            parsed_logs.append(parsed_line)
    return parsed_logs, list(set(keys_found))


def log_viewer(logfile: str, lines: int = 200):
    filename = Path(logfile).stem
    with st.container():
        st.header(f"{filename.upper()} Log:")
        log = open("logs/application.log", "+r", encoding="utf-8")
        lines = tail("logs/application.log", n=100)
        st.write(f"{len(lines)} lines")
        dictlines, keys = parse_log_lines(lines)
        st.write(f"{len(dictlines)} dict lines")
        logview = pd.DataFrame(lines, columns=["Log Lines"])
        st.dataframe(logview, use_container_width=True, height=800, hide_index=True)
