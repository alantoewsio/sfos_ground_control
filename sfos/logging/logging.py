from __future__ import annotations

import inspect
import json
import logging
import os

from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Callable, TypeVar
from typing_extensions import ParamSpec

from sfos.static import Level, constants as _c
from sfos.logging.methods import resp2dict

# Generics for decorators
P = ParamSpec("P")
R = TypeVar("R")


log_path = "./logs"
log_file: str = os.path.join(log_path, "application.log")
_init_called = False


def caller_name(stacklevel: int = 1) -> str:
    stacklevel += 1
    return inspect.stack()[stacklevel][3]


def init_logging(level: Level):
    global log_path, log_file, _init_called
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_handler = RotatingFileHandler(log_file, maxBytes=20 * _c.MB, backupCount=5)

    logging.addLevelName(5, "TRACE")
    logging.basicConfig(
        level=level.value,
        format=_c.LOG_FORMAT,
        datefmt=_c.LOG_DATE_FORMAT,
        handlers=[file_handler],
    )
    logging.log(level.value, "Logging Initialized")
    _init_called = True


def mimic_paramspec(copy_from: Callable[P, R]) -> None:
    if copy_from:
        pass

    def _decorate(fn: Callable) -> Callable[P, R]:
        def _wrap(*args, **kwargs):
            return fn(*args, **kwargs)

        return _wrap

    return _decorate


def trace(
    *messages: str | list,
    stacklevel: int = 1,
    **kwargs: str | int | list,
) -> None | Exception | object:
    return log(Level.TRACE, *messages, stacklevel=stacklevel + 1, **kwargs)


def debug(
    *messages: str | list,
    stacklevel: int = 1,
    **kwargs: str | int | list,
) -> None | Exception | object:
    return log(Level.DEBUG, *messages, stacklevel=stacklevel + 1, **kwargs)


def error(
    *messages: str | list | object,
    stacklevel: int = 1,
    **kwargs: str | int | list,
) -> None | Exception | object:

    return log(Level.ERROR, *messages, stacklevel=stacklevel + 1, **kwargs)


def info(
    *messages: str | list,
    stacklevel: int = 1,
    **kwargs: str | int | list,
) -> None | Exception | object:
    return log(Level.INFO, *messages, stacklevel=stacklevel + 1, **kwargs)


def log(
    level: Level = Level.DEBUG,
    *messages: str | list,
    stacklevel: int = 1,
    **kwargs: str | int | list,
) -> None | Exception | object:
    global _init_called
    if level == Level.NONE or not _init_called:
        return
    level = Level.DEBUG if level is None else level
    ret_obj = None
    ret_error = None
    idx = 0
    for item in messages:
        if isinstance(item, Exception):
            ret_error = item
            break
        elif hasattr(item, "error") and isinstance(item.error, Exception):
            ret_error = item.error
            ret_obj = item
            break
        idx += 1
    if ret_obj:
        if hasattr(ret_obj, "trace"):
            kwargs["trace"] = ret_obj.trace
        if hasattr(ret_obj, "success"):
            kwargs["success"] = ret_obj.success
        if hasattr(ret_obj, "fw") and ret_obj.fw is not None:
            kwargs["host"] = ret_obj.fw.address.hostname
            kwargs["port"] = ret_obj.fw.address.port
            kwargs["verify_tls"] = ret_obj.fw.address.verify_tls
        if hasattr(ret_obj, "message"):
            kwargs["msg"] = ret_obj.message
        if hasattr(ret_obj, "timer"):
            kwargs["timer"] = ret_obj.timer
        if level == Level.TRACE:
            if hasattr(ret_obj, "response") and ret_obj.response is not None:
                kwargs["response"] = json.dumps(resp2dict(ret_obj.response))

    positional_args = (
        [message for message in messages if isinstance(message, str)]
        if messages
        else []
    )
    kw_args = [f'{key}="{str(value)}"' for key, value in kwargs.items()]
    message = positional_args
    message.extend(kw_args)
    if ret_error:
        logging.exception(ret_error, stacklevel=stacklevel + 1)
    else:
        logging.log(level.value, message, stacklevel=stacklevel + 1)

    return ret_obj if ret_obj else ret_error if ret_error else None


def trace_calls(
    level: Level = Level.TRACE, log_args: bool = False, log_return: bool = False
) -> None:
    def _decorate(fn: Callable[P, R]) -> Callable[P, R]:
        fnname = fn.__name__
        sig = str(inspect.signature(fn))
        class_fn = "self" in sig

        def _wrap(*args, **kwargs):
            log(
                level,
                "<<pre>>",
                call_args=str(args) if log_args else len(args),
                call_kwargs=str(kwargs) if log_args else len(kwargs),
                stacklevel=2,
            )
            tstart = datetime.now()
            try:
                _ex = None
                this = fn
                if class_fn:
                    this = getattr(args[0], fnname)
                    args = list(args)
                    args.pop(0)
                    print("calling", this.__name__, "args", args)

                result = this(*args, **kwargs)
                has_return = result is not None
                ret_type = f' type="{type(result)}'
                ret_value = f' value="{result}"' if log_return else ""

            except Exception as e:
                _ex = e
                has_return = False
                ret_type = f' type="{type(e)}'
                ret_value = f' exception="{str(e)}"'
            finally:
                timer = (
                    f' time="{int((datetime.now() - tstart).microseconds / 1000)} ms"'
                )
                log(
                    level,
                    "<<post>>",
                    timer=timer,
                    has_return=has_return,
                    raised_exception=str(type(_ex)) if _ex else "",
                    ret_type=ret_type,
                    ret_value=ret_value,
                    stacklevel=2,
                )
                if _ex:
                    raise _ex
            return result

        return _wrap

    return _decorate
