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
import os as _os
import re as _re

from dotenv import load_dotenv as _load_dotenv
from html.parser import HTMLParser as _html_parser
from io import StringIO as _string_io
from os import environ
from requests import Request, Response
from requests.utils import dict_from_cookiejar as _dict_from_cookiejar


def load_env_file(filename: str, *vars: str | tuple[str, str]) -> dict:
    assert _load_dotenv(filename, verbose=True, override=True)
    result = {}
    for var in vars:
        default = None
        if isinstance(var, tuple):
            key, default = var
            result[key.lower()] = environ.get(key.upper(), default)
        else:
            result[var.lower()] = environ.get(var.upper())
    return result


def resp2dict(response: Response, _root: bool = True):
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
        print(msg)
        response_dict["exception"] = msg
    return response_dict


def req2dict(request: Request):
    d = {
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
        "cookies": _dict_from_cookiejar(request.cookies),
        "params": request.params,
        "data": request.data,
    }
    return d


def save_file(data: str, save_as: str | None = None) -> None:
    if save_as is None:
        return
    fname = modify_filename(save_as)

    if fname:
        f = open(fname, "w")
        f.write(data)
        f.close()


def save_dict(data: dict, save_as: str | None = None) -> None:
    if save_as is None:
        return
    msg = json.dumps(data, indent=2)
    save_file(msg, save_as)


def save_response(response: Response, save_as: str | None = None) -> None:
    if save_as is None:
        return
    response_dict = resp2dict(response)
    save_dict(response_dict, save_as)


def get_sample(filename: str) -> str:
    """Accepts:
    filename: str   The name of a file located in tests/samples

    Returns:
    File contents as str
    """
    try:
        contents: str | None = None
        with open(f"./test/samples/{filename}") as f:
            contents = f.read()
            f.close
        return contents

    except FileNotFoundError as e:
        raise FileNotFoundError from e

    except Exception as e:
        raise Exception from e


class _StripHTML(_html_parser):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = _string_io()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

    def strip(self, html: str | int | list) -> str:
        self.feed(str(html))

        stripped = self.get_data()
        return stripped

    def abbreviate(self, text: str, max_len: int | None = 100) -> str:
        # replace line breaks and tabs with spaces
        text = text.replace("\r", " ")
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        # remove repetitive spaces
        text = _re.sub(r" +", " ", text)
        if max_len:
            text = text[:max_len]
        return text

    def __call__(self, html: str | int | list, max_len: int = 100) -> str:
        result = self.strip(html)
        result = self.abbreviate(result, max_len)
        return result


html_stripper = _StripHTML()


def modify_filename(
    filename: str | None,
    *,
    prefix: str = "",
    suffix: str = "",
) -> str | None:
    """Returns the given filename with the prefix inserted at the start of the filename
    and after the path, if present, and the suffix inserted between the filename and
    file extension.

    Accepts:
    The function takes three parameters:
        filename (str)              the original filename string.
                                    If 'None', function returns None
        prefix (str) default = ""   the string to be appended between the
                                    path and the filename
        suffix (str) default = ""   the string to be appended between the
                                    filename and the file extension

    Explanation:
        It uses the os.path.split() function to split the filename into the directory
         path (dir_path) and the base filename (base_filename). This handles the case
         where the filename includes a path or not.

        It then uses the os.path.splitext() function to split the base_filename into
         the base name (base_name) and the file extension (extension).

        The modified filename is constructed by joining the dir_path, prefix,
         base_name, suffix, and extension using the os.path.join() function. This
         ensures that the appropriate path separators are used based on the operating
         system.

        Finally, the function returns the modified filename string.

    Here are a few examples of how to use the function:
        # Example 1: Filename with path
        filename = "/path/to/file.txt"
        prefix = "new_"
        suffix = "_modified"
        modified_filename = modify_filename(filename, prefix, suffix)
        print(modified_filename)  # Output: /path/to/new_file_modified.txt

        # Example 2: Filename without path
        filename = "document.pdf"
        prefix = "updated_"
        suffix = "_final"
        modified_filename = modify_filename(filename, prefix, suffix)
        print(modified_filename)  # Output: updated_document_final.pdf

        # Example 3: Filename without path or extension
        filename = "data"
        prefix = "processed_"
        suffix = "_output"
        modified_filename = modify_filename(filename, prefix, suffix)
        print(modified_filename)  # Output: processed_data_output"""
    if not filename:
        return None
    # Split the filename into directory path, base filename, and extension
    dir_path, base_filename = _os.path.split(filename)
    base_name, extension = _os.path.splitext(base_filename)

    # Construct the modified filename
    modified_filename = _os.path.join(dir_path, prefix + base_name + suffix + extension)

    return modified_filename
