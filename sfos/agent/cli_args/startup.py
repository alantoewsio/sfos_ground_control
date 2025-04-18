"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

import argparse as _args
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
from sfos.logging.logging import Level, init_logging, logtrace

ArgActions: TypeAlias = Literal[
    "info",
    "query",
    "firmware-check",
    "firmware-update",
    "password-check",
    "run-script",
]
HELP_DESC = (
    "GroundControl Agent 1.0\n"
    "An automation library for\n"
    "WebAdmin actions in Sophos Firewall (SFOS)"
)
HELP_FULL_FOOTER = """Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""
HELP_SHORT_FOOTER = """Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0. See LICENSE file for full info"""
# Used for positional type hinting in init_cli return


APRoot: TypeAlias = _ap
APCommand: TypeAlias = _ap
APQuery: TypeAlias = _ap
APReport: TypeAlias = _ap
APScript: TypeAlias = _ap
Parsers: TypeAlias = tuple[APRoot, APCommand, APQuery, APReport, APScript]


def _init_parser(
    prog: str = "", add_help: bool = True, epilog: str = HELP_SHORT_FOOTER
) -> _ap:
    return _ap(
        description=HELP_DESC,
        prog=prog,
        epilog=epilog,
        allow_abbrev=True,
        add_help=add_help,
    )


def init_cli() -> Parsers:
    """Defines the argparse CLI arguments accepted by gccli.py
    Returns (p_root, p_command, p_query, p_report, p_script)"""
    parsers = (
        _init_parser(add_help=False, epilog=HELP_FULL_FOOTER),
        _init_parser("gc command"),
        _init_parser("gc query"),
        _init_parser("gc report"),
        _init_parser("gc script"),
    )
    (p_root, p_command, p_query, p_report, p_script) = parsers
    p_root = _setup_root(p_root)
    p_command = _setup_cmd(p_command)
    p_query = _setup_query(p_query)
    p_report = _setup_report(p_report)
    p_script = _setup_script(p_script)
    return (p_root, p_command, p_query, p_report, p_script)


def read_root_args(
    root_args: list[str] | None = None, parsers: Parsers | None = None
) -> tuple[list[Connector], _args.Namespace, str]:
    """Read and evaluate the gccli.py launch arguments

    Args:
        args (list[str]): The argparse namespace used to capture CLI arguments
    """
    if parsers is None:
        parsers = init_cli()

    # break parser objects out for direct reference
    (p_root, p_cmd, p_query, p_report, p_script) = parsers
    p_dict = {
        "command": p_cmd,
        "query": p_query,
        "report": p_report,
        "script": p_script,
        "noop": None,
        "help": None,
    }
    main_args, action_args = p_root.parse_known_args(root_args)

    # Set log level
    if main_args.verbose:
        print("Runing with DEBUG logging enabled")
        init_logging(Level.DEBUG)
    elif main_args.trace:
        print("Running with TRACE logging enabled")
        init_logging(Level.TRACE)
    else:
        init_logging(Level.INFO)

    # If help flag set, append it to action_args, in case
    # another action command is provided, so the right
    # action parser can respond to help requests
    if main_args.help:
        logtrace("Help argument found. adding -h to action_args")
        action_args.append("-h")
        firewalls = []
    elif not main_args.query and not main_args.report:
        # load default credentials if provided, and firewall inventory
        # Not required for queries and reports
        logtrace("Checking arguments for creds and firewalls")
        creds = read_cred_args(main_args)
        firewalls = read_firewall_inventory(main_args, creds)
    else:
        firewalls = []

    # Determne which action to perform
    if main_args.command:
        logtrace("command argument found. root action = 'command'")
        action = "command"
    elif main_args.query:
        logtrace("query argument found. root action = 'query'")
        action = "query"
    elif main_args.report:
        logtrace("report argument found. root action = 'report'")
        action = "report"
    elif main_args.script:
        logtrace("script argument found. root action = 'script'")
        action = "script"
    elif main_args.noop:
        logtrace("noop argument found. root action = 'noop'")
        action = "noop"
    elif main_args.help:
        logtrace("help argument found. root action = 'help'")
        p_root.print_help()
        action = "Help"
        action_args = []
    elif firewalls:
        logtrace("Firewall inventory found. Defaulting to action = 'command' 'refresh'")
        # Default choice if host or inventory was provided
        action = "command"
        action_args = ["refresh"]
    else:
        logtrace("No action argument or inventory. Defaulting to action = 'Help'")
        # Show root help if no other arguments given
        p_root.print_help()
        action = "Help"
        action_args = []

    # Select the correct argument parser for the users desired action
    parser = p_dict[action] if action in p_dict else None

    # Parse the given arguments and return:
    # firewalls, action arguments, action name,
    # and any remaining arguments
    action_args, remaining_args = (
        parser.parse_known_args(action_args) if parser else ([], [])
    )
    return firewalls, action_args, action, remaining_args
