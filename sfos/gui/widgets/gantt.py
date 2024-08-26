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
import altair as alt
import pandas as pd

# source = pd.DataFrame(
#     [
#         {"task": "A", "start": 1, "end": 3},
#         {"task": "B", "start": 3, "end": 8},
#         {"task": "C", "start": 8, "end": 10},
#     ]
# )


@st.cache_data
def gantt_chart(data: pd.DataFrame):
    """A Streamlit Gantt chart

    Args:
        data (pd.DataFrame): e.g.:
        pd.DataFrame(
            [
                {"task": "A", "start": 1, "end": 3},
                {"task": "B", "start": 3, "end": 8},
                {"task": "C", "start": 8, "end": 10},
            ]
        )
    """
    chart = alt.Chart(data).mark_bar().encode(x="start", x2="end", y="task")
    st.altair_chart(chart, theme=None, use_container_width=True)
