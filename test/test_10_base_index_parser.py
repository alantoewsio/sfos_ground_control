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

import json
import pytest

from sfos.objects.firewall_info import (
    FirewallInfo as _firewall_info,
    IndexParser as _ip,
)
from sfos.static import patterns as _iv


from sfos.static import exceptions as _ex
from test.tools import get_sample

sample_files = ["test_v20_ga_index.jsp"]


@pytest.fixture(params=sample_files)
def sample(request) -> str:
    return get_sample(request.param)


def test_compiled_regex(sample: str) -> None:
    search_text = sample  # get_sample(file)
    # find script blocks
    scr_ipts = _iv.RE_TO_FIND_SCRIPTS.findall(search_text)
    assert len(scr_ipts) > 10

    # find subscr_iptions
    subs = _iv.RE_TO_FIND_SUBSCRIPTIONS.search(search_text)
    assert subs is not None
    d_subs = json.loads(subs[_iv.GROUP_SUBSCRIPTIONS])
    assert isinstance(d_subs, list)
    assert len(d_subs) == 10

    # check subscr_iption contains all expected names
    found_subs = [sub["Name"] for sub in d_subs if "Name" in sub]
    expected_subs = [
        "Base Firewall",
        "Network Protection",
        "Web Protection",
        "Email Protection",
        "Web Server Protection",
        "ZeroDay Protection",
        "Central Orchestration",
        "Enhanced Support",
        "Enhanced Plus Support",
    ]
    assert found_subs == expected_subs

    # check csrf default regex
    found_csrf = _iv.RE_TO_FIND_CSRF_KEY_VALUE_DEFAULT.search(search_text)
    assert found_csrf is not None
    assert found_csrf.group(_iv.GROUP_CSRF_KEY_VALUE) == "3ms4cmcc89ol1l1atfcsqft6r9"

    # check jsp vars regex
    vars = _iv.RE_TO_FIND_JSP_VARS.findall(search_text)
    assert len(vars) > 10

    # Un-comment to see more output while testing
    # assert False


def test_index_parser_methods(sample: str) -> None:
    search_text = sample  # get_sample(file)
    tester = _ip()
    tester._search_for_pattern(_iv.RE_TO_FIND_CSRF_KEY_VALUE_DEFAULT, search_text)


def test_index_parser_call(sample: str) -> None:
    search_text = sample  # get_sample(file)
    read_index = _ip()
    try:
        result = read_index(search_text)
        assert isinstance(result, _firewall_info)
        assert result.csrf_token == "3ms4cmcc89ol1l1atfcsqft6r9"
        assert result.displayModel == "SFVUNL"
        assert result.displayVersion in [
            "SFOS 20.0.0 GA-Build222",
        ]
        assert result.version in ["20.0.0.222"]
        assert result.applianceKey == "V01001AZAZAZ999"
        assert result.companyName == "Sophos Ltd"

    except _ex.ProcessorError as e:
        print(f"Unexpected error type:{type(e)} message:'{e}'")
        assert False

    # Un-comment to see more output while testing
    # assert False
