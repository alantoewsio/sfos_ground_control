"""SFOS Ground Control.

Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

# pylint: disable=broad-exception-caught
from __future__ import annotations

import inspect
import json
import logging
import os
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from typing import Callable, TypeAlias, TypeVar

# Disabled unused import error, since importing json_fix activates it.
# It does not get called explicitly.
import json_fix  # noqa: F401
from attr import dataclass
from typing_extensions import ParamSpec

from sfos.logging.methods import resp2dict
from sfos.static import Level
from sfos.static import constants as _c

# Generics for decorators
P = ParamSpec("P")
R = TypeVar("R")
MessageType: TypeAlias = str | list | object | Level


@dataclass
class State:
    """Global variables."""

    init_called: bool = False
    timers: dict = {}


logstate = State()

LOG_PATH = "./logs"
LOG_FILENAME = "application.log"

INIT_CALLED = False
# FrameInfo tuple value position indexes
FI_FRAME = 0
FI_FILENAME = 1
FI_LINENO = 2
FI_FUNCTION = 3
FI_CODE_CONTEXT = 4
IF_INDEX = 5


def caller_name(stacklevel: int = 1) -> str:
    """Get the name of the calling function"""
    stacklevel += 1
    return inspect.stack()[stacklevel][3]


def init_logging(level: Level) -> None:
    """Initialize default logger."""
    # global LOG_PATH, log_file, INIT_CALLED
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    log_file = os.path.join(LOG_PATH, LOG_FILENAME)
    file_handler = RotatingFileHandler(log_file, maxBytes=20 * _c.MB, backupCount=5)

    logging.addLevelName(5, "TRACE")
    logging.basicConfig(
        level=level.value,
        format=_c.LOG_FORMAT,
        datefmt=_c.LOG_DATE_FORMAT,
        handlers=[file_handler],
    )
    logging.log(level.value, "Logging Initialized")
    logstate.init_called = True


def mimic_paramspec(copy_from: Callable[P, R]) -> None:
    """Decorator to mimic another function's type hints"""
    if copy_from:
        pass

    def _decorate(fn: Callable) -> Callable[P, R]:
        def _wrap(*args, **kwargs):
            return fn(*args, **kwargs)

        return _wrap  # type: ignore

    return _decorate  # type: ignore


def logtrace(
    *messages: MessageType,
    stacklevel: int = 1,
    **kwargs: str | int | list | bool | None,
) -> None | Exception | object:
    """Write a trace log entry

    Args:
        stacklevel (int, optional): _description_. Defaults to 1.

    Returns:
        None | Exception | object: _description_
    """
    return log(*messages, level=Level.TRACE, stacklevel=stacklevel + 1, **kwargs)


def logdebug(
    *messages: str | list,
    stacklevel: int = 1,
    **kwargs: str | int | list | bool | None,
) -> None | Exception | object:
    """Write a debug log entry

    Args:
        stacklevel (int, optional): _description_. Defaults to 1.

    Returns:
        None | Exception | object: _description_
    """
    return log(*messages, level=Level.DEBUG, stacklevel=stacklevel + 1, **kwargs)


def logerror(
    *messages: MessageType,
    stacklevel: int = 1,
    **kwargs: str | int | list | bool | None,
) -> None | Exception | object:
    """Write an error log entry"""

    return log(*messages, level=Level.ERROR, stacklevel=stacklevel + 1, **kwargs)


def loginfo(
    *messages: MessageType,
    stacklevel: int = 1,
    **kwargs: str | int | list | bool | None,
) -> None | Exception | object:
    """Write an info log entry

    Args:
        stacklevel (int, optional): _description_. Defaults to 1.

    Returns:
        None | Exception | object: _description_
    """
    return log(*messages, level=Level.INFO, stacklevel=stacklevel + 1, **kwargs)


def log(
    *messages: MessageType,
    stacklevel: int = 1,
    level: Level = Level.DEBUG,
    **kwargs: str | int | list | bool | None,
) -> None | Exception | object:
    """Write a log entry

    Args:
        level (Level, optional): _description_. Defaults to Level.DEBUG.
        stacklevel (int, optional): _description_. Defaults to 1.

    Returns:
        None | Exception | object: _description_
    """
    msgs = []

    for itm in messages:
        if isinstance(itm, Level):
            level = itm
        else:
            msgs.append(itm)

    if level == Level.NONE or not logstate.init_called:
        return
    level = Level.DEBUG if level is None else level
    ret_obj = None
    ret_error = None
    idx = 0
    for i, item in enumerate(msgs):
        if isinstance(item, Exception):
            ret_error = msgs.pop(i)
            break
        elif hasattr(item, "error") and isinstance(item.error, Exception):  # type: ignore
            ret_error = item.error  # type: ignore
            ret_obj = item
            break
        idx += 1
    if ret_obj:
        if hasattr(ret_obj, "trace"):
            kwargs["trace"] = ret_obj.trace  # type: ignore
        if hasattr(ret_obj, "success"):
            kwargs["success"] = ret_obj.success  # type: ignore
        if hasattr(ret_obj, "fw") and ret_obj.fw is not None:  # type: ignore
            kwargs["host"] = ret_obj.fw.address.hostname  # type: ignore
            kwargs["port"] = ret_obj.fw.address.port  # type: ignore
            kwargs["verify_tls"] = ret_obj.fw.address.verify_tls  # type: ignore
        if hasattr(ret_obj, "message"):
            kwargs["msg"] = ret_obj.message  # type: ignore
        if hasattr(ret_obj, "timer"):
            kwargs["timer"] = ret_obj.timer  # type: ignore
        if level == Level.TRACE:
            if (
                hasattr(
                    ret_obj,
                    "response",
                )
                and ret_obj.response is not None
            ):  # type: ignore
                kwargs["response"] = json.dumps(
                    resp2dict(ret_obj.response)  # type: ignore
                )

    positional_args = (
        [msg for msg in msgs if isinstance(msg, MessageType)] if msgs else []
    )

    kw_args = [
        f'{k}="{str(v)}"' if isinstance(v, MessageType) else f"'{type(v)}'"
        for k, v in kwargs.items()
    ]
    log_msgs = positional_args
    log_msgs.extend(kw_args)
    for msg in log_msgs:
        if not isinstance(msg, str) and hasattr(msg, "__str__"):
            msg = str(msg)
        elif not isinstance(msg, str):
            print("msg object is not string, it's", type(msg))
    if isinstance(log_msgs, str):
        message = log_msgs
    else:
        message = " ".join([str(msg) for msg in log_msgs]) if log_msgs else ""
    message = message.replace("\r", "").replace("\n", "\\n")
    if ret_error:
        logging.exception(ret_error, stacklevel=stacklevel + 1)
    else:
        logging.log(level.value, message, stacklevel=stacklevel + 1)

    return ret_obj if ret_obj else ret_error if ret_error else None


def log_callstart(
    level: Level = Level.TRACE,
    verbose: bool = False,
    stacklevel: int = 1,
):
    """Log information about the function call and the timestapm of the call

    Args:
        level (Level, optional): _description_. Defaults to Level.TRACE.
        verbose (bool, optional): _description_. Defaults to False.
        stacklevel (int, optional): _description_. Defaults to 1.
    """

    current_frame = inspect.currentframe()
    frames = inspect.getouterframes(frame=current_frame)

    # FrameInfo(frame, filename, lineno, function, code_context, in dex) is returned.
    ancestry: list[str] = []
    for f in frames:
        ancestry.append(f[FI_FUNCTION])

    caller = frames[-2]
    caller_args = inspect.getargvalues(caller[FI_FRAME])

    arg_dict = caller_args.__dict__
    args = [
        f"arg_{k}{f"='{v}'" if verbose else str(type(v))}" for k, v in arg_dict.items()
    ]
    logstate.timers[caller[FI_FUNCTION]] = datetime.now(tz=UTC)
    log(level=level, args=args, verbose=verbose, stacklevel=stacklevel + 1)


def log_calldone(
    level: Level = Level.TRACE, verbose: bool = False, stacklevel: int = 1, **kwargs
):
    """log info about the call near its completion, and log the time taken in ms if
    log_callstart was called earlier

    Args:
        level (Level, optional): _description_. Defaults to Level.TRACE.
        verbose (bool, optional): _description_. Defaults to False.
        stacklevel (int, optional): _description_. Defaults to 1.
    """
    frames = inspect.getouterframes(1, context=1)
    caller = frames[-2]
    timer = -1
    if caller[FI_FUNCTION] in logstate.timers:
        timer = (
            datetime.now - logstate.timers[caller[FI_FUNCTION]]
        ).total_seconds() * 1000
        del logstate.timers[caller[FI_FUNCTION]]

    timer = f"{timer:f}ms" if timer >= 0 else "-"
    log(level=level, verbose=verbose, timer=timer, stacklevel=stacklevel + 1, **kwargs)
