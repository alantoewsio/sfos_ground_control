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

from __future__ import annotations
import json
from datetime import datetime, UTC
from typing import Literal
from requests import (
    Session as _session,
    Response as _response,
    exceptions as _req_ex,
)
from requests.utils import (
    dict_from_cookiejar as _dict_from_cookiejar,
    cookiejar_from_dict as _cookiejar_from_dict,
)
import urllib3

from sfos.base import (
    exceptions as _ex,
    FirewallInfo as _fwi,
    parse_index as _parse_index,
    ServiceAddress as _sa,
    SfosMode as _req_mode,
)
from sfos.webadmin.methods import make_sfos_request as _make_req, load_definition

from sfos.webadmin.sfos_request import SfosRequest as _req

urllib3.disable_warnings()

# key name definitions
USERNAME = "username"
PASSWORD = "password"
CAPTCHA = "captcha"
JSESSIONID = "JSESSIONID"
CSRF_TOKEN = "X-Csrf-Token"
AUTH_SUCCESS_MSG = '{"redirectionURL":"/webpages/index.jsp","status":200}'
AUTH_FAIL_MSG = '{"redirectionURL":"/webpages/login.jsp","status":-1}'
AUTH_DISCLAIMER_MSG = '"disclaimer_message":"'


class SfosResponse:
    def __init__(
        self,
        *,
        trace: str,
        fw: Connector | None = None,
        request: _req | None = None,
        response: _response | None = None,
        error: Exception | None = None,
        data: dict | _fwi | None = None,
        success: bool | None = None,
    ) -> None:
        self.fw = fw
        self.request = request
        self.response = response
        self.error = error
        self.data = data
        self.status_code = response.status_code if response else None
        self.timestamp = str(datetime.now(tz=UTC))
        self.text = None
        self.success = None
        self.trace = trace
        if self.error:
            self.success = success if success else False
            self.text = f"ERROR {str(error)}"

        elif self.response:
            self.success = (
                success if success else self.response.status_code in range(200, 300)
            )
            self.text = response.text if response.text else ""
            if data:
                self.data = data
            else:
                try:
                    self.data = json.loads(self.text)
                except Exception:
                    self.data = None
        elif data:
            self.success = success if success else True
            self.data = data


class Connector:
    def __init__(
        self,
        address: _sa | None = None,
        credentials: dict | None = None,
        hostname: str | None = None,
        port: int | None = None,
        verify_tls: bool | None = None,
        username: str | None = None,
        password: str | None = None,
        resume_session: dict | None = None,
    ) -> None:
        if hostname:
            self.address = _sa(
                hostname, port or 4444, verify_tls if verify_tls is not None else True
            )
        else:
            self.address = address
        self.cookies = None
        self.credentials: dict | None = None
        if username and password:
            credentials = {"username": username, "password": password}
        self._set_creds(credentials)
        self.info: _fwi | None = None
        self.csrf_token = None
        self._logging_in = False
        self.session = None

        # Captcha raises an error and returns
        # an image to be interpreted by the user.
        # The captcha response must be returned
        # with the same JSESSIONID
        if (
            resume_session
            and JSESSIONID in resume_session
            and (CAPTCHA in credentials or CSRF_TOKEN in resume_session)
        ):
            self.cookies[JSESSIONID] = resume_session[JSESSIONID]

    def target(self) -> str:
        return f"{self.credentials[USERNAME]}@{self.address.address}"

    def _set_creds(self, credentials: dict | None = None) -> None:
        if not credentials:
            return
        if USERNAME not in credentials or PASSWORD not in credentials:
            return
        self.credentials = credentials

    def _get_creds(self) -> dict:
        assert self.credentials
        creds_data = {
            USERNAME: self.credentials[USERNAME],
            PASSWORD: self.credentials[PASSWORD],
            "languageid": "1",
        }
        if CAPTCHA in self.credentials:
            creds_data[CAPTCHA] = self.credentials[CAPTCHA]
        return creds_data

    def login(self, credentials: dict | None = None) -> SfosResponse:
        self._logging_in = True
        self._set_creds(credentials)
        if not self.credentials:
            return SfosResponse(
                fw=self, error=_ex.LoginError("Credentials not provided"), trace="201"
            )
        req_auth, req_token = self._get_login_req_cmds()

        # send SfosRequest one at a time to correlate with request
        self.session = _session()
        rsp_auth, rsp_token = self.send_requests(
            req_auth, req_token, session=self.session
        )
        if rsp_auth.error and isinstance(rsp_auth.error, _ex.ConnectionError):
            return SfosResponse(
                fw=self,
                error=rsp_auth.error,
                trace="205",
            )

        if AUTH_FAIL_MSG in rsp_auth.text:
            return SfosResponse(
                fw=self,
                error=_ex.LoginError(
                    "Authentication failed - Check username or password are correct"
                ),
                trace="206",
            )
        if AUTH_DISCLAIMER_MSG in rsp_auth.text:
            return SfosResponse(
                fw=self,
                error=_ex.LoginError(
                    "Authentication failed - Disclaimer Message Enabled"
                ),
                trace="207",
            )
        if AUTH_SUCCESS_MSG not in rsp_auth.text:
            return SfosResponse(
                fw=self,
                request=req_token,
                response=rsp_token,
                error=_ex.LoginError("Authentication failed - Unexpected response"),
                trace="208",
            )

        try:
            fwinfo = _parse_index(rsp_token.text)
            assert fwinfo.csrf_token is not None

        except _ex.AgentError as e:
            return SfosResponse(
                fw=self,
                request=req_token,
                response=rsp_token,
                error=_ex.LoginError(str(e)),
                trace="223",
            )

        self.info = fwinfo
        self.csrf_token = fwinfo.csrf_token
        self._logging_in = False
        return SfosResponse(
            fw=self, request=req_token, response=rsp_token, data=fwinfo, trace="229"
        )

    def get_info(self) -> SfosResponse:
        if not self.csrf_token:
            sfos_resp = self.login()
            return (
                sfos_resp
                if not sfos_resp.success
                else SfosResponse(
                    fw=self,
                    response=sfos_resp.response,
                    data=self.info,
                    success=self.info is not None,
                    trace="239",
                )
            )
        return SfosResponse(
            fw=self, success=self.info is not None, data=self.info, trace="235"
        )

    def _get_login_req_cmds(self) -> list[_req]:
        creds_data = self._get_creds()
        # convert dict to string with json whitespace removed
        creds_content = json.dumps(creds_data, separators=(",", ":"))

        # Create SfosRequest generators from definitions
        auth, token = load_definition(_req_mode.ADMIN_LOGIN)
        op_auth = _make_req(auth, self.address, creds_content)
        op_get_token = _make_req(token, self.address)

        # Generate auth requests and return them to caller
        return [op_auth, op_get_token]

    def _get_request_args(self, request: _req) -> dict:
        result = {
            "url": request.url,
            "headers": request.headers,
            "verify": request.verify,
            "timeout": request.timeout,
            "data": request.body if request.method == "post" else None,
        }
        return result

    def _ensure_session(self, session: _session | None = None) -> Literal[True]:
        self.session = session or self.session or _session()
        assert self.session is not None
        return True

    def _ensure_authenticated(self) -> Literal[True]:
        if not self.csrf_token and not self._logging_in:
            return self.login().success
        return True

    def _send_request_worker(
        self, req: _req, session: _session | None = None
    ) -> SfosResponse:

        assert self._ensure_session(session)
        if self.cookies:
            # reload saved session cookies if there are any
            cookies = _cookiejar_from_dict(self.cookies)
            self.session.cookies.update(cookies)
        if self.csrf_token:
            req.headers.pop(CSRF_TOKEN, None)
            req.headers[CSRF_TOKEN] = self.csrf_token

        # Build request arguments dict
        request_contents = self._get_request_args(request=req)
        response: _response | None = None
        try:
            if req.method == "get":
                response = self.session.get(**request_contents)
            else:
                response = self.session.post(**request_contents)
            self.cookies = _dict_from_cookiejar(
                self.session.cookies
            )  # turn cookiejar into dict
        except _req_ex.SSLError as e:
            return SfosResponse(
                fw=self,
                request=req,
                response=e.response,
                error=_ex.CertificateError(
                    "Unable to verify Certificate: ",
                    str(e),
                ),
                trace="245",
            )

        except _req_ex.ConnectTimeout as e:
            return SfosResponse(
                fw=self,
                request=req,
                response=e.response,
                error=_ex.ConnectionTimeoutError(
                    f"{self.address.address}: Connection timed out",
                    self.address.address,
                ),
                trace="247",
            )

        except _req_ex.ConnectionError as e:
            if "NameResolutionError" in str(e):
                this_ex = _ex.NameResolutionError(
                    f"'{self.address.hostname}': Name resolution failed",
                )
            else:
                this_ex = _ex.ConnectionError(
                    f"'{self.address.hostname}': Connection error",
                )
            return SfosResponse(
                fw=self,
                request=req,
                response=e.response,
                error=this_ex,
                trace="246",
            )
        return SfosResponse(fw=self, response=response, trace="252")

    def send_request(self, req: _req, session: _session | None = None) -> SfosResponse:
        self._ensure_authenticated()
        response = self._send_request_worker(req, session)
        return response

    def send_requests(
        self, *reqs: _req, session: _session | None = None
    ) -> list[SfosResponse]:
        assert self._ensure_authenticated()
        responses = [self._send_request_worker(req, session) for req in reqs]
        return responses
