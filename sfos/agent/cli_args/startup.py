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

import argparse
from argparse import ArgumentParser as _ap
from typing import Literal, TypeAlias

from sfos.agent.methods import (
    read_cred_args,
    read_firewall_inventory,
)
from sfos.agent.cli_args.command_args import setup_command_arguments as _setup_cmd
from sfos.agent.cli_args.query_args import setup_query_arguments as _setup_query
from sfos.agent.cli_args.report_args import setup_report_arguments as _setup_report
from sfos.agent.cli_args.script_args import setup_script_arguments as _setup_script
from sfos.agent.cli_args.root_args import setup_root_arguments as _setup_root
from sfos.webadmin.connector import Connector


DATE_FMT = "%Y-%m-%d"
ArgActions: TypeAlias = Literal[
    "info",
    "query",
    "firmware-check",
    "firmware-update",
    "password-check",
    "run-script",
]
h_desc = (
    "GroundControl Agent 1.0\n"
    "An automation library for\n"
    "WebAdmin actions in Sophos Firewall (SFOS)"
)
h_foot = "Copyright 2024 Sophos Inc. All Rights Reserved."

_root: TypeAlias = _ap
_command: TypeAlias = _ap
_query: TypeAlias = _ap
_report: TypeAlias = _ap
_script: TypeAlias = _ap

Parsers: TypeAlias = tuple[_root, _command, _query, _report, _script]


def _init_parser(prog: str = "", add_help: bool = True) -> _ap:
    return _ap(
        description=h_desc,
        prog=prog,
        epilog=h_foot,
        allow_abbrev=True,
        add_help=add_help,
    )


def init_cli_parsers() -> Parsers:
    """returns (root, commmand, query, report, script)"""
    parsers = (
        _init_parser(add_help=False),
        _init_parser("gc command"),
        _init_parser("gc query"),
        _init_parser("gc report"),
        _init_parser("gc script"),
    )

    return parsers


def init_cli() -> Parsers:
    """Defines the argparse CLI arguments accepted by gccli.py"""
    parsers = init_cli_parsers()
    (p_root, p_command, p_query, p_report, p_script) = parsers
    p_root = _setup_root(p_root)
    p_command = _setup_cmd(p_command)
    p_query = _setup_query(p_query)
    p_report = _setup_report(p_report)
    p_script = _setup_script(p_script)

    return (p_root, p_command, p_query, p_report, p_script)


def read_root_args(
    root_args: list[str] | None = None, parsers: Parsers | None = None
) -> tuple[list[Connector], argparse.Namespace, str]:
    """Read and evaluate the gccli.py launch arguments

    Args:
        args (list[str]): The argparse namespace used to capture CLI arguments
    """
    if not parsers:
        parsers = init_cli()
    (p_root, p_cmd, p_query, p_report, p_script) = parsers
    args, rest = p_root.parse_known_args(root_args)
    # print("read_root_args: ", root_args, args)
    creds = read_cred_args(args)
    firewalls = read_firewall_inventory(args, creds)

    if args.help:
        rest.append("-h")

    if args.command:
        return firewalls, p_cmd.parse_args(rest), "command"
    elif args.query:
        return firewalls, p_query.parse_args(rest), "query"
    elif args.report:
        return firewalls, p_report.parse_args(rest), "report"
    elif args.script:
        return firewalls, p_script.parse_args(rest), "script"
    elif args.noop:
        return firewalls, None, "noop"
    elif args.help:
        p_root.print_help()
        return [], None, "help"
    else:
        return firewalls, p_cmd.parse_args(["refresh"]), "command"
