""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing
permissions and limitations under the License.
"""

import pytest
from sfos.base import (
    ServiceAddress as _sa,
    SfosMode as _req_mode,
    SfosOperation as _req_oper,
)
from sfos.webadmin import methods as _m
from sfos.webadmin.definition import Definition as _def


@pytest.fixture
def address() -> _sa:
    return _sa("testhost")


@pytest.fixture
def headers_get() -> dict:
    return {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "{HOST}:{PORT}",
        "User-Agent": "{USER_AGENT}",
    }


@pytest.fixture
def headers_post() -> dict:
    return {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "{HOST}:{PORT}",
        "User-Agent": "{USER_AGENT}",
        "Accept": "text/plain, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "{ROOT_URL}",
    }


@pytest.fixture
def headers_post_prepped() -> dict:
    return {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "testhost:4444",
        "User-Agent": "GroundControl/1.0",
        "Accept": "text/plain, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://testhost:4444/",
        "Referer": "https://testhost:4444/webconsole/webpages/login.jsp",
    }


@pytest.fixture
def auth_def() -> _def:
    t_headers = _m.get_common_headers("post")
    return _def(
        **{
            "req_mode": _req_mode.ADMIN_LOGIN,
            "req_operation": _req_oper.NONE,
            "web_path": "{PATH_CONTROLLER}",
            "web_method": "post",
            "web_headers": {**t_headers, "Referer": "{LOGIN_URL}"},
            "urlencode": True,
        }
    )


@pytest.fixture
def auth_data() -> dict:
    return '{"username":"admin","password":"Secret+Pass!","languageid":"1"}'


@pytest.fixture
def auth_request() -> str:
    return (
        "mode=151&"
        "json=%7B%22username%22%3A%22admin%22"
        "%2C%22password%22%3A%22Secret%2BPass%21%22"
        "%2C%22languageid%22%3A%221%22%7D&"
        "__RequestType=ajax"
    )


@pytest.fixture
def header_vars() -> dict:
    return {
        "HostPort": "{HOST}:{PORT}",
        "Port": "{PORT}",
        "User-Agent": "{USER_AGENT}",
        "Root-Url": "{ROOT_URL}",
        "Controller-Url": "{CONTROLLER_URL}",
        "Index-Jsp-Url": "{INDEX_JSP_URL}",
        "Login-Url": "{LOGIN_URL}",
        "Unchanged-Value": "No Change!",
    }


##################################################


def test_get_common_headers_get(headers_get: dict) -> None:
    t_headers = _m.get_common_headers("get")
    e_headers = headers_get

    assert t_headers == e_headers


def test_get_common_headers_post(headers_post: dict) -> None:
    t_headers = _m.get_common_headers("post")
    e_headers = headers_post
    assert t_headers == e_headers


def test_prepare_req_headers(header_vars: dict) -> None:
    t_address = _sa("testhost")
    t_headers = header_vars
    e_prepped = {
        "HostPort": "testhost:4444",
        "Port": "4444",
        "User-Agent": "GroundControl/1.0",
        "Root-Url": "https://testhost:4444/",
        "Controller-Url": "https://testhost:4444/webconsole/Controller",
        "Index-Jsp-Url": "https://testhost:4444/webconsole/webpages/index.jsp",
        "Login-Url": "https://testhost:4444/webconsole/webpages/login.jsp",
        "Unchanged-Value": "No Change!",
    }
    t_prepped = _m._prepare_req_headers(t_headers, t_address)

    assert t_prepped == e_prepped


def test_get_file_str() -> None:
    t_txt = _m.load_file_str("sample.txt", "./test/samples/")
    e_txt = "This is a test file."
    assert t_txt == e_txt


def test_get_json_dict() -> None:
    t_dict = _m.load_json_data("test_21_sample.json", "./test/samples/")
    e_dict = {"command": "test", "request_object": "request_object_data", "data": None}
    assert t_dict == e_dict


def test_get_request_def(auth_def: _def) -> None:
    t_def, t_token = _m.load_definition(_req_mode.ADMIN_LOGIN)
    e_def = auth_def

    assert t_def.req_mode == e_def.req_mode
    assert t_def.req_operation == e_def.req_operation
    assert t_def.web_method == e_def.web_method
    assert t_def.path == e_def.path
    assert t_def.urlencode == e_def.urlencode
    assert t_def.web_headers == e_def.web_headers


def test_prepare_req_content(auth_def: _def, auth_data: auth_data) -> None:
    t_def = auth_def
    t_data = auth_data
    t_parts = _m._prepare_request_conent(t_def, t_data)
    e_parts = [
        "mode=151",
        (
            "json=%7B%22username%22%3A%22admin%22"
            "%2C%22password%22%3A%22Secret%2BPass%21%22"
            "%2C%22languageid%22%3A%221%22%7D"
        ),
        "__RequestType=ajax",
        "t=",
    ]
    assert t_parts[0] == e_parts[0]
    assert t_parts[1] == e_parts[1]
    assert t_parts[2] == e_parts[2]
    assert t_parts[3].startswith(e_parts[3])


def test_assemble_req_content(
    auth_def: _def, auth_data: dict, auth_request: str
) -> None:
    t_def = auth_def
    t_data = auth_data
    t_content = _m._assemble_request_content(t_def, t_data)
    e_content = auth_request
    assert t_content.startswith(e_content)


def test_make_request(
    auth_def: _def,
    address: _sa,
    auth_data: str,
    auth_request: str,
    headers_post_prepped: dict,
) -> None:
    t_def = auth_def
    t_address = address
    t_data = auth_data
    t_req = _m.make_sfos_request(t_def, t_address, t_data)

    assert t_req.url == "https://testhost:4444/webconsole/Controller"
    assert t_req.headers == headers_post_prepped
    assert t_req.body.startswith(auth_request)
    assert t_req.verify is True
    assert t_req.method == "post"
