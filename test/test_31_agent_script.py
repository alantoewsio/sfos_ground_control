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

from sfos.agent import (
    Script,
    ScriptItem,
    load_script,
    execute_script,
)
from sfos.base import ServiceAddress as _sa
from sfos.webadmin import (
    Connector as _connector,
    make_sfos_request_from_template as _make_sfos_request_from_template,
    SfosRequest as _req,
)
from test.tools import load_env_file


def init_test_vars() -> dict:
    result = load_env_file(
        "./test/samples/test_30.env",
        *[
            ("TEST_HOST", "172.16.16.16"),
            ("test_port", 4444),
            ("TEST_TLS", "True"),
            ("TEST_USER", "admin"),
            ("TEST_PASS", ""),
            ("TEST_BAD_PASS", ""),
        ],
    )
    return result


vars = init_test_vars()


@pytest.fixture
def script1() -> Script:
    return load_script(r".\test\samples\test_40_script.sfos")


@pytest.fixture
def address() -> _sa:
    return _sa(vars["test_host"], vars["test_port"], verify_tls=vars["test_tls"])


@pytest.fixture
def good_creds() -> dict:
    return {"username": vars["test_user"], "password": vars["test_pass"]}


@pytest.fixture
def fw(address: _sa, good_creds: dict) -> _connector:
    return _connector(address, good_creds)


def test_script_item(address: _sa) -> None:
    t_si = ScriptItem(command="HEARTBEAT_STATUS", request_object="hbStatus")
    e_si = {
        "command": "HEARTBEAT_STATUS",
        "request_object": "hbStatus",
        "data": None
    }
    assert t_si == e_si
    host = f'{vars["test_host"]}:{vars["test_port"]}'
    t_req = _make_sfos_request_from_template(**t_si, address=address)[0]
    e_req = _req(
        url=f"https://{vars["test_host"]}:{vars["test_port"]}/webconsole/Controller",
        headers={
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": f"{host}",
            "User-Agent": "GroundControl/1.0",
            "Accept": "text/plain, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": f"https://{host}/",
            "Referer": f"https://{host}/webconsole/webpages/login.jsp",
            "X-Requested-With": "XMLHttpRequest"

        },
        body="mode=1322&requestObj={'hbStatus': 1}&__RequestType=ajax&t=",
        method="post",
        verify=False,
        timeout=10,
    )
    assert t_req.url == e_req.url
    assert t_req.method == e_req.method
    assert t_req.verify is e_req.verify
    assert t_req.timeout == e_req.timeout
    assert t_req.body.startswith(e_req.body)
    assert t_req.headers == e_req.headers


def test_script_load(script1: Script) -> None:
    t_script = script1

    e_script = {
        'commands': [
            {
                'command': 'HEARTBEAT_STATUS',
                'request_object': 'hbStatus',
                'data': None
            }
        ]
    }
    assert t_script == e_script


def test_run_script(fw: _connector, script1: Script) -> None:
    t_script = script1
    results = execute_script(fw=fw, script=t_script,)

    assert isinstance(results, list)
    assert len(results) == 1
    result = results[0]

    assert result.success is True
    assert result.status_code == 200

    print("data type:", type(result.data))
    assert isinstance(result.data, dict)
    e_data = {
        'hbStatus': {
            'registered': True,
            'hbEnabled': True,
            'status': {
                'red': '0',
                'green': 0,
                'missing': 0,
                'yellow': '0'
            }
        }
    }
    t_data = result.data

    # assert "hbStatus" in t_data
    assert t_data == e_data
