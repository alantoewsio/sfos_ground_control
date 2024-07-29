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

from sfos.agent.methods import (
    load_json_data as _load_json,
)
from sfos.objects import CustomDict as _cdict
from sfos.static import SfosMode as _req_mode
from sfos.webadmin import (
    Connector,
    SfosResponse as _sresp,
    make_sfos_request_from_template,
    load_request_object_data,
)


class ScriptItem(_cdict):
    def __init__(
        self,
        command: str | _req_mode,
        request_object: str | None = None,
        data: dict | None = None,
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
    ) -> list[_sresp]:
        return execute_script(fw, self)


def load_script(filename: str) -> Script:
    script = Script(_load_json(filename))
    return script


def execute_script_item(
    fw: Connector,
    item: ScriptItem,
    state: dict | None = None,
) -> list[_sresp]:

    cmd = item["command"]
    req_obj = item["request_object"]
    req_object_def = load_request_object_data(cmd, req_obj) if req_obj else None
    data = apply_state_vars(item["data"], state)

    script_items = make_sfos_request_from_template(
        command=cmd,
        request_object=req_object_def,
        address=fw.address,
        data=data,
    )
    return fw.send_requests(*script_items)


def apply_state_vars(data: dict, state: dict | None = None) -> dict:
    if state is None:
        return data

    updated = {k: v.format(**state) for k, v in data.items() if isinstance(v, str)}
    recurse = {
        k: apply_state_vars(v, state) for k, v in data.items() if isinstance(v, dict)
    }
    preserved = {
        k: v.format(**state)
        for k, v in data.items()
        if k not in updated and k not in recurse
    }
    result = dict(updated, **recurse, **preserved)

    return result


def execute_script(fw: Connector, script: Script) -> list[_sresp]:
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

        (
            script_items.extend(reqs)
            if isinstance(reqs, list)
            else script_items.append(reqs)
        )

    return fw.send_requests(*script_items)
