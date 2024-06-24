from __future__ import annotations
import json
import os
import time
from requests import Session
from typing import Literal
from urllib import parse

from sfos.base import (
    exceptions as _ex,
    SfosMode as _req_mode,
    SfosOperation as _req_oper,
    ServiceAddress as _sa,
)

from sfos.webadmin.definition import Definition as _srdef
from sfos.webadmin.sfos_request import SfosRequest as _req


separators = {True: "&", False: "\n"}
REQ_TEMPLATE_PATH = "./sfos/webadmin/templates/requests/"
OBJECT_PATH = "./sfos/webadmin/templates/req_objects/"
HEADER_PATH = "./sfos/webadmin/templates/headers/"
REQ_OBJECTS = "req_objects"

header_defs = {
    "common": "headers_common.json",
    "get": "headers_common_get.json",
    "post": "headers_common_post.json",
}


def get_common_headers(method: Literal["get", "post"], path: str = HEADER_PATH) -> dict:
    h_common = load_json_data(header_defs["common"], path)
    h_method = load_json_data(header_defs[method], path)
    return {**h_common, **h_method}


def _find_file(name: str, paths: list[str]) -> str:
    for path in paths:
        this = os.path.join(path, name)
        if os.path.exists(this):
            return path
    return None


def load_request_object_data(
    command: str | _req_mode,
    name: str,
    path: str | list[str] = OBJECT_PATH,
) -> dict:
    if isinstance(name, dict):
        return name
    path = path or OBJECT_PATH
    # make sure command is a string value
    if isinstance(command, _req_mode):
        command = command.name
    # make sure it has the correct extension
    command = command if command.endswith(".json") else f"{command}.json"
    # if multiple paths given, find one where the file exists
    path = _find_file(name, path) if isinstance(path, list) else path

    # if file doesn't exist, raise an error
    if not path or not os.path.exists(os.path.join(path, command)):
        raise _ex.NoMatchFound(f"No request object found for '{command}'")

    # load the object from file
    data = load_json_data(name=command, path=path)
    if name not in data["req_objects"]:
        raise _ex.NoMatchFound(f"Request object '{name}' not found for '{command}'")
    return data["req_objects"][name]


def load_definition(
    name: str | _req_oper,
    path: str | list[str] = REQ_TEMPLATE_PATH,
    header_path: str | list[str] = HEADER_PATH,
) -> _srdef | list[_srdef]:
    path = path or REQ_TEMPLATE_PATH
    header_path = header_path or HEADER_PATH
    if isinstance(name, _req_mode):
        name = name.name
    name = name if name.endswith(".json") else f"{name}.json"
    path = _find_file(name, path) if isinstance(path, list) else path
    if path is None:
        raise _ex.DefinitionNotFound("Definition not found:", name)

    def_data = load_json_data(name, path)
    if isinstance(def_data, list):
        return [_dict_to_def(item) for item in def_data]
    else:
        return _dict_to_def(def_data)


def _dict_to_def(
    req_dict: dict,
    header_path: str | list[str] = HEADER_PATH,
) -> _srdef | list[_srdef]:
    header_path = header_path or HEADER_PATH
    common_headers = get_common_headers(req_dict["web_method"], header_path)

    # convert int to enum
    if "req_mode" in req_dict:
        req_dict["req_mode"] = _req_mode(req_dict["req_mode"])
    else:
        req_dict["req_mode"] = _req_mode.NONE

    if "req_operation" in req_dict:
        req_dict["req_operation"] = _req_oper(req_dict["req_operation"])
    else:
        req_dict["req_operation"] = _req_oper.NONE

    # add common method headers
    req_dict["web_headers"] = {**common_headers, **req_dict["web_headers"]}
    req_def = _srdef(**req_dict)

    return req_def


def load_json_data(name: str, path: str = REQ_TEMPLATE_PATH) -> dict | list:
    path = path or REQ_TEMPLATE_PATH
    json_str = load_file_str(name, path)
    json_obj = json.loads(json_str)
    return json_obj


def load_file_str(filename: str, path: str) -> str:
    """Accepts:
    filename: str   The name of a file located in sfos/webadmin/templates/requests

    Returns:
    File contents as Definition
    """
    try:
        contents: str | None = None
        with open(os.path.join(path, filename)) as f:
            contents = f.read()
            f.close
        return contents

    except FileNotFoundError as e:
        raise FileNotFoundError from e

    except Exception as e:
        raise Exception from e


def _prepare_req_headers(headers: dict[str, str], address: _sa) -> dict[str, str]:
    replacements = {
        "USER_AGENT": "GroundControl/1.0",
        "HOST": address.hostname,
        "PORT": address.port,
        "ROOT_URL": address.url_base,
        "CONTROLLER_URL": address.url_controller,
        "INDEX_JSP_URL": address.url_index_jsp,
        "LOGIN_URL": address.url_login_jsp,
    }

    results = {}
    for header, value in headers.items():
        if isinstance(value, str):
            results[header] = value.format(**replacements)
        else:
            results[header] = value
    return results


def _prepare_request_conent(
    definition: _srdef, req_data: str | None = None
) -> list[str]:
    # Prepare all SfosRequest components:
    # [mode=x, operation=y, json=z, __requesttype=ajax],

    # Early return if no req_data
    if definition.req_mode == _req_mode.NONE:
        return []

    result = [f"mode={str(definition.req_mode.value)}"]
    if definition.req_operation != _req_oper.NONE:
        result.append("operation=" + str(definition.req_operation.value))
    if definition.req_object:
        result.append("requestObj=" + str(definition.req_object))
    if req_data and (definition.web_method == "get" or definition.urlencode):
        # req_data becomes query string if method = get or urlencode is enabled
        if not isinstance(req_data, str):
            req_data = json.dumps(req_data)
        req_data = parse.quote(req_data)
    if req_data:
        result.append(f"json={req_data}")

    result.append("__RequestType=ajax")
    result.append(f"t={int(time.time())}")
    return result


def _assemble_request_content(definition: _srdef, req_data: str | None = None) -> str:
    """Assembles a SfosRequest by preparing its individual parts,
    then assembling the list of parts into a final string"""

    # Prepare all SfosRequest components
    result = _prepare_request_conent(definition, req_data)
    if result == []:
        return ""
    separator = definition.separator or separators[definition.urlencode]

    # combine result list into a single string
    req_content = separator.join(result)

    return req_content


def make_sfos_request_from_template(
    command: str,
    address: _sa,
    request_object: str | None = None,
    data: str | None = None,
    command_paths: list[str] | None = None,
) -> list[_req]:
    command_paths = command_paths or REQ_TEMPLATE_PATH

    req_defs = load_definition(command, command_paths)
    if request_object:
        req_defs.req_object = load_request_object_data(command, request_object)

    if isinstance(req_defs, list):
        return [make_sfos_request(req_def, address, data) for req_def in req_defs]
    else:
        return [make_sfos_request(req_defs, address, data)]


def make_sfos_request(
    definition: _srdef,
    address: _sa,
    data: str | None = None,
) -> _req:
    """Compiles the SfosRequest data, url, method, and headers
    needed to execute the SfosRequest"""

    url = None
    data = _assemble_request_content(definition, data)
    if definition.web_method == "get":
        url = address.url(definition.path, data)
        data = None
    else:
        url = address.url(definition.path)

    data = _req(
        url=url,
        headers=_prepare_req_headers(definition.web_headers, address),
        method=definition.web_method,
        body=data,
        verify=address.verify_tls,
        timeout=address.timeout,
    )
    return data


def download_file(session: Session, url: str):
    local_filename = url.split("/")[-1]
    # NOTE the stream=True parameter below
    with session.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename


def download(session: Session, url: str, file_path="", attempts=2):
    """Downloads a URL content into a file (with large file support by streaming)

    :param url: URL to download
    :param file_path: Local file name to contain the data downloaded
    :param attempts: Number of attempts
    :return: New file path. Empty string if the download failed
    """
    if not file_path:
        file_path = os.path.realpath(os.path.basename(url))

    url_sections = parse.urlparse(url)
    if not url_sections.scheme:
        url = f"http://{url}"
    for attempt in range(1, attempts + 1):
        try:
            if attempt > 1:
                os.time.sleep(10)  # 10 seconds wait time between downloads
            with session.get(url, stream=True) as response:
                response.raise_for_status()
                with open(file_path, "wb") as out_file:
                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):  # 1MB chunks
                        out_file.write(chunk)
                return file_path
        except Exception as ex:
            print(f"Attempt #{attempt} failed with error: {ex}")
    return ""
