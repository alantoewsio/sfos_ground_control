"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

# pylint: disable=broad-exception-caught

from __future__ import annotations
import json
import json_fix  # noqa: F401

from datetime import datetime

# import trace
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

from sfos.logging.logging import logtrace, logerror
from sfos.objects import SfosResponse
from sfos.objects.firewall_info import FirewallInfo as _fwi, parse_index as _parse_index
from sfos.static import exceptions as _ex, SfosMode as _req_mode, constants as _c
from sfos.webadmin.methods import (
    make_sfos_request as _make_req,
    load_definition,
)
from sfos.objects.service_address import ServiceAddress as _sa
from sfos.objects.sfos_request import SfosRequest as _req

urllib3.disable_warnings()


class Connector:
    """Encapsulate a connection to the webadmin interface of an SFOS firewall"""

    def __init__(
        self,
        address: _sa | None = None,
        credentials: dict[str, str] | None = None,
        hostname: str | None = None,
        port: int | None = None,
        verify_tls: bool | None = None,
        username: str | None = None,
        password: str | None = None,
        resume_session: dict | None = None,
        timeout: int = 2,
    ) -> None:
        if hostname:
            self.address = _sa(
                hostname,
                port or 4444,
                verify_tls if verify_tls is not None else True,
                timeout,
            )
        else:
            self.address = address
        self.cookies = {}
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
            and _c.JSESSIONID in resume_session
            and (
                _c.CAPTCHA in credentials  # type: ignore
                or _c.CSRF_TOKEN in resume_session
            )
        ):
            self.cookies[_c.JSESSIONID] = resume_session[_c.JSESSIONID]

    def target(self) -> str:
        """username and address of target connection

        Returns:
            str: {username}@{address}
        """
        return f"{self.credentials[_c.USERNAME]}@{self.address.address}"  # type: ignore

    def _set_creds(self, credentials: dict | None = None) -> None:
        if not credentials:
            return
        if _c.USERNAME not in credentials or _c.PASSWORD not in credentials:
            return
        self.credentials = credentials

    def _get_creds(self) -> dict:
        assert self.credentials
        creds_data = {
            _c.USERNAME: self.credentials[_c.USERNAME],
            _c.PASSWORD: self.credentials[_c.PASSWORD],
            "languageid": "1",
        }
        if _c.CAPTCHA in self.credentials:
            creds_data[_c.CAPTCHA] = self.credentials[_c.CAPTCHA]
        return creds_data

    def login(self, credentials: dict | None = None) -> SfosResponse:
        """login to SFOS firewal webadmin interface

        Args:
            credentials (dict | None, optional): _description_. Defaults to None.

        Returns:
            SfosResponse: _description_
        """
        self._logging_in = True
        self._set_creds(credentials)
        if not self.credentials:
            result = SfosResponse(
                fw=self,
                error=_ex.LoginError("Credentials not provided"),
                trace="201",
            )
            logerror(result)
            return result

        req_auth, req_token = self._get_login_req_cmds()  # type: ignore

        # send SfosRequest one at a time to correlate with request
        self.session = _session()
        rsp_auth, rsp_token = self.send_requests(
            req_auth, req_token, session=self.session
        )

        if rsp_auth.error and isinstance(rsp_auth.error, _ex.AgentConnectionError):
            result = SfosResponse(
                fw=self,
                error=rsp_auth.error,
                trace="205",
            )
            logerror(result)
            return result

        if rsp_auth.text and _c.AUTH_FAIL_MSG in rsp_auth.text:
            result = SfosResponse(
                fw=self,
                error=_ex.LoginError("Incorrect username or password"),
                trace="206",
            )

            logerror(result)
            return result
        if rsp_auth.text and _c.AUTH_DISCLAIMER_MSG in rsp_auth.text:
            result = SfosResponse(
                fw=self,
                error=_ex.LoginError("Blocked by disclaimer"),
                trace="207",
            )
            logerror(result)
            return result
        if rsp_auth.status_code == "200" and _c.AUTH_SUCCESS_MSG not in rsp_auth.text:
            result = SfosResponse(
                fw=self,
                request=req_token,
                response=rsp_token.response,
                error=_ex.LoginError("Unexpected auth response"),
                trace="208",
            )
            logerror(result)
            return result

        try:
            assert rsp_token.text
            fwinfo = _parse_index(rsp_token.text)
            assert fwinfo.csrf_token is not None
            hostname = self.address.hostname if self.address else "?"
            logtrace(
                host=hostname,
                login=rsp_auth.success,
                msg=rsp_auth.text,
                csrf_token=fwinfo.csrf_token,
            )
        except _ex.AgentError as e:
            result = SfosResponse(
                fw=self,
                request=req_token,
                response=rsp_token.response,
                error=_ex.LoginError(str(e)),
                trace="223",
            )
            logerror(result)
            return result

        self.info = fwinfo
        self.csrf_token = fwinfo.csrf_token
        self._logging_in = False
        return SfosResponse(
            fw=self,
            request=req_token,
            response=rsp_token.response,
            data=fwinfo,
            trace="229",
        )

    def get_info(self) -> SfosResponse:
        """Get login response info from firewall"""
        tstart = datetime.now()
        if not self.csrf_token:
            sfos_resp = self.login()
            if not sfos_resp.success:
                return sfos_resp

        timer = int((datetime.now() - tstart).microseconds / 1000)
        return SfosResponse(
            fw=self,
            request=sfos_resp.request if sfos_resp else None,  # type: ignore
            response=sfos_resp.response if sfos_resp else None,  # type: ignore
            data=self.info,
            success=self.info is not None,
            timer=timer,
            trace="239",
        )

    def _get_login_req_cmds(self) -> list[_req]:
        if not self.address:
            logerror("No address")
            return []

        creds_data = self._get_creds()
        # convert dict to string with json whitespace removed
        creds_content = json.dumps(creds_data, separators=(",", ":"))

        auth_creds_def = None
        get_token_def = None
        # Create SfosRequest generators from definitions
        login_actions = load_definition(_req_mode.ADMIN_LOGIN)
        if isinstance(login_actions, list) and len(login_actions) == 2:
            auth_creds_def, get_token_def = login_actions
        else:
            logerror("Unexcpected result: Check ADMIN_LOGIN definition is correct")
            return []

        op_auth = _make_req(auth_creds_def, self.address, creds_content)
        op_get_token = _make_req(get_token_def, self.address)

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
            results = self.login()
            if not results.success and results.error:
                raise results.error
            elif not results.success:
                raise _ex.AgentConnectionError("Unable to authenticate")

        return True

    def send_request(self, req: _req, session: _session | None = None) -> SfosResponse:
        tstart = datetime.now()
        assert self._ensure_session(session)
        if self.cookies and self.session:
            # reload saved session cookies if there are any
            cookies = _cookiejar_from_dict(self.cookies)
            self.session.cookies.update(cookies)
        if self.csrf_token:
            req.headers.pop(_c.CSRF_TOKEN, None)
            req.headers[_c.CSRF_TOKEN] = self.csrf_token

        # Build request arguments dict
        request_contents = self._get_request_args(request=req)
        response: _response | None = None
        error = None
        trace = 200
        try:
            self._ensure_authenticated()
            if not self.session:
                raise _req_ex.ConnectionError("Not Authenticated")
            if req.method == "get":
                method = self.session.get
            else:
                method = self.session.post
            if req.special == "download":
                with method(stream=True, **request_contents) as r:
                    r.raise_for_status()
                    if (
                        "Content-Disposition" in r.headers
                        and "filename=" in r.headers["Content-Disposition"]
                    ):
                        fn_header = str(r.headers["Content-Disposition"])
                        filename = fn_header.split("filename=")[1]
                        filename = f"{filename}.sfos"
                    else:
                        filename = "unknown.sfos"
                    print("downloading", filename)
                    with open(filename, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            # If you have chunk encoded response uncomment if
                            # and set chunk_size parameter to None.
                            # if chunk:
                            f.write(chunk)
                        return SfosResponse(
                            success=True,
                            data={"action": "download", "file": filename},
                            trace=f"conn-{trace}",
                        )
            else:
                response = method(**request_contents)

            self.cookies = _dict_from_cookiejar(
                self.session.cookies
            )  # turn cookiejar into dict

        except _req_ex.SSLError:
            error = (245, _ex.CertificateError("Invalid Certificate"))

        except _req_ex.ConnectTimeout:
            error = (246, _ex.ConnectionTimeoutError("Connection timed out"))

        except _req_ex.ConnectionError as e:
            ex = (
                _ex.NameResolutionError("DNS Error")
                if "NameResolutionError" in str(e)
                else _ex.AgentConnectionError(f"Connection error: '{e}'")
            )
            error = (247, ex)

        finally:
            timer = int((datetime.now() - tstart).microseconds / 1000)
            if error:
                (trace, error) = error

        return SfosResponse(
            fw=self,
            request=req,
            response=response,
            error=error,
            timer=timer,
            trace=f"conn-{trace}",
        )

    def send_requests(
        self, *reqs: _req, session: _session | None = None
    ) -> list[SfosResponse]:
        """Get the results of sent Web requests

        Args:
            session (_session | None, optional): _description_. Defaults to None.

        Returns:
            list[SfosResponse]: _description_
        """
        responses = [self.send_request(req, session) for req in reqs]
        return responses
