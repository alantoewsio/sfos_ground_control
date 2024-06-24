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

import json
from requests import Response


from sfos.agent.methods import (
    load_json_data as _load_json,
    response_to_dict as _resp2dict,
)
from sfos.base import CustomDict as _cdict, SfosMode as _req_mode
from sfos.webadmin import (
    Connector,
    make_sfos_request_from_template,
    load_request_object_data,
)


class ScriptItemResponse(_cdict):
    def __init__(self, response: Response, fw: Connector):
        result = {}
        result["target"] = fw.address.address
        result["status"] = response.status_code in range(200, 300)
        result["status_code"] = response.status_code
        result["response_raw"] = _resp2dict(response)
        result["data"] = {}
        try:
            resp_data = json.loads(response.text)
            result["data"] = resp_data
        except Exception:
            pass

        super().__init__(result)


class ScriptItem(_cdict):
    def __init__(
        self,
        command: str | _req_mode,
        request_object: str | None = None,
        data: dict | None = None,
        option_def_path: list[str] | None = None,
    ):

        item = {
            "command": command,
            "request_object": request_object,
            "data": data,
        }
        super().__init__(item)


class Script(_cdict):

    def __init__(self, commands: list[dict] = [], from_file: str | None = None):
        if from_file:
            commands.extend(_load_json(from_file))
        items = []
        items.extend([ScriptItem(**command) for command in commands])
        script = {"commands": items}
        super().__init__(script)

    def execute(
        self,
        fw: Connector,
        state: dict | None = None,
    ) -> list[ScriptItemResponse]:
        return execute_script(fw, self, state)


def load_script(filename: str, state: dict | None = None) -> Script:
    script = Script(_load_json(filename))
    return script


def execute_script_item(
    fw: Connector,
    item: ScriptItem,
    state: dict | None = None,
) -> list[ScriptItemResponse]:

    cmd = item["command"]
    req_obj = item["request_object"]
    req_object_def = load_request_object_data(cmd, req_obj) if req_obj else None
    data = item["data"]
    script_items = make_sfos_request_from_template(
        command=cmd,
        request_object=req_object_def,
        address=fw.address,
        data=data,
    )
    try:
        responses = fw.send_requests(*script_items)
        return _format_response(responses=responses, fw=fw)
    except Exception as e:
        print(
            f"Command Error: target:{fw.address} command:{cmd} error:{e} type:{type(e)}"
        )
    return []


def execute_script(
    fw: Connector, script: Script, state: dict | None = None
) -> list[ScriptItemResponse]:
    # print(f"execute received script with {len(script)} commands")
    script_items = []

    for item in script["commands"]:
        cmd = item["command"]
        req_obj = item["request_object"]
        req_object_def = load_request_object_data(cmd, req_obj) if req_obj else None
        data = item["data"]
        reqs = make_sfos_request_from_template(
            command=cmd,
            request_object=req_object_def,
            address=fw.address,
            data=data,
        )
        try:
            if isinstance(reqs, list):
                script_items.extend(reqs)
            else:
                script_items.append(reqs)
            responses = fw.send_requests(*script_items)
            return _format_response(responses=responses, fw=fw)
        except Exception as e:
            print(
                (
                    f"Command Error: target:{fw.address} "
                    f"command:{cmd} "
                    f"error:{e} "
                    f"type:{type(e)}"
                )
            )
        return []


def _format_response(
    responses: list[Response], fw: Connector
) -> list[ScriptItemResponse]:
    ret = []
    for response in responses:
        if not isinstance(response, Response):
            print(f"response is {type(response)} - expected {type(Response)}")
        ret.append(ScriptItemResponse(response, fw))
    return [ScriptItemResponse(response, fw=fw) for response in responses]
