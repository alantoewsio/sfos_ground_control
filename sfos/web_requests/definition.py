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
from typing import Literal

from sfos.base import SfosMode as _req_mode, SfosOperation as _req_oper


class Definition:
    def __init__(
        self,
        req_mode: _req_mode,
        req_operation: _req_oper = _req_oper.NONE,
        req_object: str | None = None,
        web_path: str | None = None,
        web_method: Literal["get", "post"] = "post",
        web_headers: dict[str, str] = {},
        urlencode: bool | None = None,
        arguments: dict | None = None,
    ):

        # Constants
        self.PATH_CONTROLLER = "webconsole/Controller"
        self.PATH_INDEX_JSP = "webconsole/webpages/index.jsp"
        self.PATH_LOGIN_JSP = "webconsole/webpages/login.jsp"
        self.path = web_path or self.PATH_CONTROLLER

        self.req_mode = req_mode
        self.req_operation = req_operation
        self.req_Request_object = req_object
        self.web_method: Literal["get", "post"] = web_method
        self.web_headers = web_headers
        self.urlencode = urlencode or web_method == "get"
        self.arguments = arguments
