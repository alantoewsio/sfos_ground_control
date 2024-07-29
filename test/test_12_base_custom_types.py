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
import pytest
from sfos.static import exceptions as _ex
from sfos.objects.custom_types import (
    Boolean,
    TrueOrFalse,
    YesOrNo,
    OnOrOff,
    EnableOrDisable,
    EnabledOrDisabled,
    CustomDict,
)


@pytest.fixture
def foo_bar() -> dict[bool, str]:
    return {True: "foo", False: "bar"}


@pytest.fixture
def t_bool(foo_bar: dict[bool, str]) -> Boolean:
    return Boolean(foo_bar)


def test_boolean_true_during_init(foo_bar: dict[bool, str]) -> None:
    # Assign during init
    t_data = {"value": Boolean(foo_bar, True)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": "foo"}'


def test_boolean_false_during_init(foo_bar: dict[bool, str]) -> None:
    t_data = {"value": Boolean(foo_bar, False)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": "bar"}'


def test_boolean_none_during_init(foo_bar: dict[bool, str]) -> None:
    t_data = {"value": Boolean(foo_bar, None)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": null}'


def test_boolean_true_after_init(t_bool: Boolean) -> None:
    # Assign after init
    t_data = {"value": t_bool(True)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": "foo"}'


def test_boolean_false_after_init(t_bool: Boolean) -> None:
    t_data = {"value": t_bool(False)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": "bar"}'


def test_boolean_none_after_init(t_bool: Boolean) -> None:
    t_data = {"value": t_bool(None)}
    t_result = json.dumps(t_data)
    assert t_result == '{"value": ""}'


def test_boolean_children_true() -> None:
    value = True
    t_data = {
        "a": TrueOrFalse(value),
        "b": YesOrNo(value),
        "c": OnOrOff(value),
        "d": EnableOrDisable(value),
        "e": EnabledOrDisabled(value),
    }
    t_result = json.dumps(t_data)
    assert (
        t_result
        == '{"a": "true", "b": "yes", "c": "on", "d": "enable", "e": "enabled"}'
    )


def test_boolean_children_false() -> None:
    value = False
    t_data = {
        "a": TrueOrFalse(value),
        "b": YesOrNo(value),
        "c": OnOrOff(value),
        "d": EnableOrDisable(value),
        "e": EnabledOrDisabled(value),
    }
    t_result = json.dumps(t_data)
    assert (
        t_result
        == '{"a": "false", "b": "no", "c": "off", "d": "disable", "e": "disabled"}'
    )


def test_boolean_str_true_after_init(t_bool: Boolean) -> None:
    t_bool("foo")
    print("comparing with bool(t_bool) is True")
    assert bool(t_bool) is True
    print("comparing with 'is'")
    assert t_bool.as_bool is True


def test_boolean_str_false_after_init(t_bool: Boolean) -> None:
    t_bool("bar")
    print("comparing with bool(t_bool) is False")
    assert bool(t_bool) is False
    assert t_bool.as_bool is False


def test_boolean_str_bad(t_bool: Boolean) -> None:
    with pytest.raises(_ex.NoMatchFound):
        t_bool("bad")


def test_custom_dict_init() -> None:
    t_data = {"key1": "value1", "key2": 2, "key3": YesOrNo(True)}
    t_dict = CustomDict(t_data)

    assert t_dict["key1"] == "value1"
    assert t_dict["key2"] == 2
    assert str(t_dict["key3"]) == "yes"
    assert bool(t_dict["key3"]) is True


def test_custom_dict_type_preservation() -> None:
    t_data = {"key1": "value1", "key2": 2, "key3": YesOrNo(True)}
    t_dict = CustomDict(t_data)
    t_dict["key3"] = "no"
    assert isinstance(t_dict["key3"], YesOrNo)
    assert bool(t_dict["key3"]) is False


def test_custom_dict_immutability() -> None:
    t_data = {"key1": "value1", "key2": 2, "key3": YesOrNo(True)}
    t_dict = CustomDict(t_data)
    with pytest.raises(_ex.InvalidParameter):
        t_dict["key4"] = "SHOULD_FAIL"
