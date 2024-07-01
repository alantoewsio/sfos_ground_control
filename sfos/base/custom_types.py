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

import json
import json_fix

from typing import Any, Literal

from sfos.base import exceptions as _ex

EMPTY_STRING = ""
true = "true"
false = "false"

if json_fix:
    pass


class CustomDict(dict):
    """Base class for dict data limited to selected keys"""

    def __init__(self, data: dict | str | None = None):
        self._initializing = False
        if data and isinstance(data, str):
            data = json.loads(data)

        if data and isinstance(data, dict):
            self._initializing = True
            for k, v in data.items():
                self[k] = v
            self._initializing = False

    def __setitem__(self, item, value):
        if not self._initializing and item not in self:
            raise _ex.InvalidParameter(f"Item {item} is not supported")
        if item in self and isinstance(self[item], Boolean):
            self[item].set_value(value)
        else:
            super().__setitem__(item, value)
        # assert self[item] == value

    def __delitem__(self, item):
        if not self._initializing and item not in self:
            return
        super().__delitem__(item)
        assert item not in self
        self.changed = True

    @property
    def __dict__(self) -> dict:
        exports = {k: v for k, v in self.items() if not str(k).startswith("_")}
        return exports

    def __json__(self) -> dict:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps(self)


class Boolean:
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': Boolean(
                    'value_pair'={
                        True:"true",
                        False:"false",
                    },
                    value=True,
                )
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'true'}"

    """

    def __init__(
        self,
        value_pair: dict[bool, str] | None = None,
        value: bool | str | None = None,
    ) -> None:
        if value_pair is None:
            raise _ex.NotConfigured(
                "'Boolean' cannot be directly instantiated - Create a child instance"
            )
        self.value_pair = value_pair
        self.value: bool | None = None
        self.set_value(value)

    def _lookup_str(self, value: str) -> bool | None:
        tval = self.value_pair[True]
        fval = self.value_pair[False]

        if value == tval:
            return True
        elif value == fval:
            return False
        elif value == EMPTY_STRING:
            return None
        else:
            raise _ex.NoMatchFound(
                f"Unknown value '{value}'. Expecting '{tval}' or '{fval}' "
            )

    def set_value(self, value: str | bool | None) -> None:
        # print(f"Setting {type(self)}: value type '{type(value)}'='{value}'")
        if isinstance(value, bool):
            self.value = value
        elif value is None:
            self.value = None
        else:
            self.value = self._lookup_str(value)

    def __call__(
        self,
        value: str | bool | None | Literal["GET_VALUE"] = "GET_VALUE",
    ) -> str:
        if value != "GET_VALUE":
            self.set_value(value)
        return self.__str__()

    # def __setattr__(self, name: str, value: Any) -> None:
    #     print(f"Boolean setattr '{name}' to '{value}'")
    #     super(type(self), self).__setattr__(name, value)

    @property
    def as_bool(self) -> bool:
        return self.__bool__() or False

    def __eq__(self, value: bool | str) -> bool:
        print("Boolean __eq__ called")
        if isinstance(value, bool):
            return value is self.value
        if self.value is None:
            return value == EMPTY_STRING
        return str(self.value).startswith(value)

    def __str__(self) -> str:
        # print("Boolean __str__ called")
        if self.value is None:
            return EMPTY_STRING
        result = self.value_pair[self.value]
        return result

    def __instancecheck__(self, instance: Any) -> bool:
        # print("instancecheck", type(instance))
        return (
            type(instance) is bool
            or type(instance) is type(self)
            or type(instance) is Boolean
        )

    # def __getattribute__(self, item: str) -> Any:
    #     print(f"Boolean __getattribute__ called for {item}")
    #     value = super(Boolean, self).__getattribute__(item)
    #     print(f"Boolean __getattribute__ returned '{item}'='{value}({type(value)})'")
    #     return value

    def __valuecheck__(self, value: str) -> bool:
        try:
            if value is EMPTY_STRING:
                return True
            self._lookup_str(value)
            return True
        except _ex.NoMatchFound:
            return False

    def __json__(self) -> str | None:
        return self.__str__() if self.value is not None else None

    def __bool__(self) -> bool:
        # print("Boolean __bool__ called.")
        return bool(self.value)

    def __repr__(self) -> str:
        # print("Boolean __repr__ called.")
        return self.__str__()


class TrueOrFalse(Boolean):
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': TrueOrFalse(True)
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'true'}"
    """

    def __init__(self, value: bool | str | None = None) -> None:
        super().__init__({True: "true", False: "false"}, value=value)


class OnOrOff(Boolean):
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': OnOrOff(True)
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'on'}"
    """

    def __init__(self, value: bool | str | None = None) -> None:
        super().__init__({True: "on", False: "off"}, value=value)


class YesOrNo(Boolean):
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': YesOrNo(True)
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'yes'}"
    """

    def __init__(self, value: bool | str | None = None) -> None:
        super().__init__({True: "yes", False: "no"}, value=value)


class EnableOrDisable(Boolean):
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': EnableOrDisable(True)
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'enable'}"
    """

    def __init__(self, value: bool | str | None = None) -> None:
        super().__init__({True: "enable", False: "disable"}, value=value)


class EnabledOrDisabled(Boolean):
    """Used to handle named boolean flags used by sfos.
    Usage:
        data={
            'value': EnabledOrDisabled(True)
            }
        print(json.dumps(data))
        # Outputs: "{'value': 'enabled'}"
    """

    def __init__(self, value: bool | str | None = None) -> None:
        super().__init__({True: "enabled", False: "disabled"}, value=value)
