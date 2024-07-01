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

import pytest

from sfos.base import (
    ServiceAddress as _sa,
    SfosMode as _req_mode,
    SfosOperation as _req_oper,
)
from sfos.webadmin.definition import Definition as _srdef
from sfos.webadmin.methods import make_sfos_request as _make_req


@pytest.fixture
def headers() -> dict:
    return {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Host": "testhost:4444",
        "Origin": "https://testhost:4444/",
        "Referer": "https://testhost:4444/",
        "User-Agent": "",
    }


@pytest.fixture
def address() -> _sa:
    return _sa("testhost")


def test_request_post(address: _sa, headers: dict) -> None:
    req_def = _srdef(
        _req_mode.TEST,
        _req_oper.TEST,
        web_path="{PATH_CONTROLLER}",
        web_headers=headers,
        web_method="post",
    )
    result = _make_req(req_def, address)
    # print(f"result={result}")
    assert result.url == "https://testhost:4444/webconsole/Controller"
    assert result.headers == {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Host": "testhost:4444",
        "Origin": "https://testhost:4444/",
        "Referer": "https://testhost:4444/",
        "User-Agent": "",
    }
    assert result.method == "post"
    assert result.timeout == 10
    assert result.verify is True
    assert result.body.startswith(
        "mode=99999\noperation=-99999\n__RequestType=ajax\nt="
    )


def test_request_get(address: _sa, headers: dict) -> None:
    req_def = _srdef(
        _req_mode.TEST,
        _req_oper.TEST,
        web_path="{PATH_CONTROLLER}",
        web_headers=headers,
        web_method="get",
    )

    result = _make_req(req_def, address)
    e_url = (
        "https://testhost:4444/webconsole/Controller?"
        "mode%3D99999%26operation%3D-99999%26__RequestType%3Dajax%26t%3D"
    )
    t_url = result.url
    print(f"resurl: {t_url}")
    assert t_url.startswith(e_url)
    assert result.headers == {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Host": "testhost:4444",
        "Origin": "https://testhost:4444/",
        "Referer": "https://testhost:4444/",
        "User-Agent": "",
    }
    assert result.body is None
    assert result.method == "get"
    assert result.timeout == 10
    assert result.verify is True
