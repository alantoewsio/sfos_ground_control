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
        separator: str | None = None,
        arguments: dict | None = None,
    ):

        # Constants
        self.PATH_CONTROLLER = "webconsole/Controller"
        self.PATH_INDEX_JSP = "webconsole/webpages/index.jsp"
        self.PATH_LOGIN_JSP = "webconsole/webpages/login.jsp"
        self.path = web_path or self.PATH_CONTROLLER

        self.req_mode = req_mode
        self.req_operation = req_operation
        self.req_object = req_object
        self.web_method: Literal["get", "post"] = web_method
        self.web_headers = web_headers
        self.urlencode = urlencode or web_method == "get"
        self.separator = separator
        self.arguments = arguments
