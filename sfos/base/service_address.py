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

from urllib import parse


class ServiceAddress:
    """Wraps the host ip or name and service port
    for quick translation into relevant variations or related urls"""

    def __init__(
        self,
        hostname: str,
        port: int = 4444,
        verify_tls: bool = True,
        timeout=10,
    ):
        self.hostname = hostname
        self.port = port
        self.verify_tls = verify_tls
        self.timeout = timeout

        # Constants
        self.PATH_CONTROLLER = "webconsole/Controller"
        self.PATH_INDEX_JSP = "webconsole/webpages/index.jsp"
        self.PATH_LOGIN_JSP = "webconsole/webpages/login.jsp"

    def __repr__(self) -> str:
        return f"'host': '{self.hostname}', 'port': {self.port}"

    def __call__(self) -> str:
        return self.address

    @property
    def address(self) -> str:
        """returns {hostname}:{port}"""
        return f"{self.hostname}:{self.port}"

    @property
    def url_base(self) -> str:
        """returns "https://{address}/"""
        return f"https://{self.address}/"

    def _prepare_path(self, path: str | None = None) -> str:
        replacements = {
            "PATH_CONTROLLER": self.PATH_CONTROLLER,
            "PATH_INDEX_JSP": self.PATH_INDEX_JSP,
            "PATH_LOGIN_JSP": self.PATH_LOGIN_JSP,
        }

        path = path or "/"
        result = path.format(**replacements)
        return result

    def url(self, path: str, params: str = "") -> str:
        """returns "https://{address}/path?params"""
        url_base = "https://" + self.address
        if not url_base.endswith("/"):
            url_base += "/"

        path = self._prepare_path(path)
        if path.startswith("/"):
            path = path[1:]

        params = "?" + parse.quote(params) if params else ""

        result = f"{url_base}{path}{params}"

        # print(f"Constructed URL {result} from '{url_base}' + '{path}' + '{params}' ")
        return result

    @property
    def url_controller(self) -> str:
        return self.url_base + self.PATH_CONTROLLER

    @property
    def url_index_jsp(self) -> str:
        return self.url_base + self.PATH_INDEX_JSP

    @property
    def url_login_jsp(self) -> str:
        return self.url_base + self.PATH_LOGIN_JSP
