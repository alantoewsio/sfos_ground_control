import json
from datetime import datetime, UTC
from requests import Response as _response
from requests.utils import dict_from_cookiejar as _dict_from_cookiejar
from typing import Any

from sfos.objects.firewall_info import FirewallInfo as _fwi
from sfos.logging import trace


class SfosResponse:

    def __init__(
        self,
        *,
        traceval: str,
        fw: Any | None = None,
        request: Any | None = None,
        response: _response | None = None,
        error: Exception | None = None,
        data: dict | _fwi | None = None,
        success: bool | None = None,
        timer: int | None = None,
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
        self.trace = traceval
        self.timer = timer
        if self.error:
            self.success = success if success else False
            self.text = str(error)
            if hasattr(self.error, "response"):
                self.response = self.error.response

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

        trace()

    @property
    def __dict__(self) -> dict:
        if isinstance(self.data, _fwi):
            data = self.data.base_info
        else:
            data = self.data
        return {
            "success": self.success,
            "host": self.fw.address,
            "status": self.status_code,
            "timestamp": self.timestamp,
            "has_error": self.error is not None,
            "trace": self.trace,
            "timer": self.timer,
            "text": self.text,
            "data": data,
            "web_response": resp2dict(self.response) if self.response else None,
        }

    def __json__(self) -> dict:
        return {"SfosResponse": self.__dict__}

    @property
    def __repr__(self) -> str:
        return json.dumps(self.__json__())

    @property
    def __str__(self) -> str:
        self.__repr__


def resp2dict(response: _response, _root: bool = True):
    response_dict = {}
    try:
        response_dict = {
            "text": response.text,
            "headers": dict(sorted(response.headers.items())),
            "cookies": dict(sorted(_dict_from_cookiejar(response.cookies).items())),
            "status_code": response.status_code,
            "request": {
                "url": response.request.url,
                "method": response.request.method,
                "headers": dict(sorted(response.request.headers.items())),
                "path_url": response.request.path_url,
                "body": response.request.body,
            },
        }
        if _root:
            response_dict["history"] = [resp2dict(h, False) for h in response.history]

    except Exception as e:
        msg = f"resp2dict Exception: type='{type(e)}' msg='{e}'"
        response_dict["exception"] = msg
    return response_dict
