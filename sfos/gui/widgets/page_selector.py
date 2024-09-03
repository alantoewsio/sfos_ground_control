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


def _pagination_callback(current_page: int):
    st.session_state["current_page"] = current_page
    st.write("refreshing..")        
    # if "current_page" not in st.session_state:


def _add_btn(
    label: str,
    current_page: int,
    key: str | None = None,
    disabled: bool = False,
):
    if not key:
        key = f"pg-{label}"
    st.button(
        label=label,
        disabled=disabled,
        key=key,
        on_click=_pagination_callback,
        use_container_width=True,
        kwargs={"current_page": current_page},
    )


@st.fragment
def pagination_controls(maxperside: int = 5):
    """Add pagination buttons"""

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    if "page_count" not in st.session_state:
        st.session_state["page_count"] = 0

    current_page = st.session_state["current_page"]
    page_count = st.session_state["page_count"]

    last_page = page_count - 1
    lbuttons = min(maxperside, current_page)
    rbuttons = min(maxperside, last_page - current_page)
    lextra = 2
    rextra = 2

    colwidths = [2] * lextra + [1] * lbuttons + [3] + [1] * rbuttons + [2] * rextra
    with st.container(height=40, border=False):

        cols = st.columns(
            colwidths,
            gap="small",
            vertical_alignment="bottom",
        )
        idx = 0
        this_page_num = current_page - lbuttons
        # first page and prev page buttons
        if lextra:
            with cols[idx]:
                _add_btn("<<", 0, disabled=not lbuttons)
            idx += 1

            with cols[idx]:
                _add_btn("<", current_page - 1, disabled=not lbuttons)
            idx += 1

        # prev (up to) maxperside page numbers
        if lbuttons:
            while this_page_num < current_page:
                with cols[idx]:
                    _add_btn(str(this_page_num + 1), this_page_num)
                this_page_num += 1
                idx += 1
        # current page
        with cols[idx]:
            _add_btn(f"**{this_page_num + 1}**", this_page_num, disabled=True)
            # t.markdown(f"**{this_page_num+1}**")
        this_page_num += 1
        idx += 1

        # next (up to) maxperside page numbers
        if rbuttons:

            while this_page_num <= (current_page + maxperside):
                if this_page_num >= page_count:
                    break
                with cols[idx]:
                    _add_btn(str(this_page_num + 1), this_page_num)
                this_page_num += 1
                idx += 1

        with cols[idx]:
            _add_btn(r"\>", current_page + 1, "pg-next", disabled=not rbuttons)
            idx += 1

        with cols[idx]:
            _add_btn(r"\>\>", last_page, "pg-last", disabled=not rbuttons)
            idx += 1


def page_selection_status():
    """Page x of y (# Rows)
    or if page_count =-1
    # Rows"""

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 0
    if "page_count" not in st.session_state:
        st.session_state["page_count"] = 0
    if "row_count" not in st.session_state:
        st.session_state["row_count"] = 0

    if st.session_state["page_count"] < -2:
        st.text(f"{st.session_state["row_count"]} Rows")
    else:
        st.text(
            f"Page {st.session_state["current_page"] + 1} of "
            f"{st.session_state["page_count"]} "
            f"({st.session_state["row_count"]} Total Rows)"
        )

def page_size_selector(page_sizes: list[int], default_index: int = 0):
    """Set the current paging size

    Args:
        page_size (int): _description_
    """

    if "page_size" not in st.session_state:
        st.session_state["page_size"] = page_sizes[default_index]
        st.write(f"page_size not set. setting to {st.session_state["page_size"]}")

    elif st.session_state["page_size"] not in page_sizes:
        st.write(f"invalid page size requested: {st.session_state["page_size"]}")
        st.session_state["page_size"] = page_sizes[default_index]

    st.selectbox(
        label="Page Size",
        options=page_sizes,
        label_visibility="hidden",
        key="page_size",
        # on_change=_page_size_callback,
    )
