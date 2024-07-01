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

from sfos.base import exceptions as _ex, ServiceAddress as _sa, FirewallInfo as _fwi
from sfos.webadmin.connector import Connector as _fw, AUTH_SUCCESS_MSG, AUTH_FAIL_MSG
from test.tools import load_env_file

from test.tools import save_response


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
def address() -> _sa:
    return _sa(vars["test_host"], vars["test_port"], verify_tls=vars["test_tls"])


@pytest.fixture
def good_creds() -> dict:
    return {"username": vars["test_user"], "password": vars["test_pass"]}


@pytest.fixture
def bad_creds() -> dict:
    return {"username": vars["test_user"], "password": vars["test_bad_pass"]}


def test_login_good(address: _sa, good_creds: dict) -> None:
    t_fw = _fw(address=address, credentials=good_creds)
    auth, token = t_fw._get_login_req_cmds()

    # send requests one at a time to correlate with request
    t_fw._logging_in = True
    rslt = t_fw.send_requests(auth, token)
    (r_auth, r_token) = rslt

    if not r_auth.text == AUTH_SUCCESS_MSG:
        save_response(r_auth.response, "test_23_1_login_good_a_auth.json")
        pytest.fail("credentials not authenticated successfully")

    if "c$rFt0k3n =" not in r_token.text:
        save_response(r_token.response, "test_23_1_login_good_b_token.json")
        pytest.fail("csrf token not found")
    assert "c$rFt0k3n =" in r_token.text


def test_login_bad_creds(address: _sa, bad_creds: dict) -> None:
    t_fw = _fw(address=address, credentials=bad_creds)
    auth, token = t_fw._get_login_req_cmds()

    sresp = t_fw.send_request(auth)
    assert sresp.text == AUTH_FAIL_MSG


def test_login_fn_good(address: _sa, good_creds: dict) -> None:
    t_fw = _fw(address=address, credentials=good_creds)

    sfos_resp = t_fw.login()
    assert sfos_resp.success
    assert sfos_resp.data is not None
    assert isinstance(sfos_resp.data, _fwi)
    assert sfos_resp.data.csrf_token is not None
    assert sfos_resp.error is None


def test_login_fn_bad(address: _sa, bad_creds: dict) -> None:
    t_fw = _fw(address=address, credentials=bad_creds)

    sresp = t_fw.login()
    assert sresp.success is False
    assert sresp.error
    assert isinstance(sresp.error, _ex.LoginError)


def test_login_fn_name_resolution_error(address: _sa, bad_creds: dict) -> None:
    t_fw = _fw(hostname="badhost", credentials=bad_creds)

    sresp = t_fw.login()
    assert sresp.success is False
    assert sresp.error
    assert isinstance(sresp.error, _ex.NameResolutionError)


def test_login_fn_timeout_error(address: _sa, bad_creds: dict) -> None:
    t_fw = _fw(_sa(hostname="10.98.76.54", timeout=1), credentials=bad_creds)

    sresp = t_fw.login()
    assert sresp.success is False
    assert sresp.error
    assert isinstance(sresp.error, _ex.ConnectionTimeoutError)
