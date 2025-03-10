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


def setup_root_arguments(parser: _ap) -> _ap:
    """Define root cli arguments

    Args:
        parser (_ap): _description_
    """
    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", default=False
    )
    parser.add_argument(
        "-vv", dest="verbose", action="store_true", default=False, help=_args.SUPPRESS
    )
    parser.add_argument(
        "-vvv", dest="trace", action="store_true", default=False, help=_args.SUPPRESS
    )
    conn = parser.add_argument_group("Connection options")
    inventory = conn.add_mutually_exclusive_group()

    help = "IP or Hostname of SFOS firewall - Cannot be used with '-i'"
    inventory.add_argument(
        "-a", "--hostname", nargs=1, dest="hostname", required=False, help=help
    )
    help = "Firewall connection information inventory list - Cannot be used with '-a'"
    inventory.add_argument(
        "-i",
        "--inventory",
        nargs="+",
        dest="inventory",
        required=False,
        help=help,
    )

    help = "Default: 4444, WebAdmin port (Allowed values: 1-65535)"
    conn.add_argument("-p", "--port", type=int, default=4444, dest="port", help=help)
    help = (
        "Disables TLS checking if set. Same as '--verify_tls False'. "
        "Overrides verify_tls if both are set. "
        "CAUTUION: Disabling TLS checks is insecure and should be avoided."
    )
    conn.add_argument(
        "--insecure",
        action="store_true",
        help=help,
    )
    help = (
        "Default: True, Use '--verify_tls False' if WebAdmin cert is self-signed. "
        "CAUTUION: Disabling TLS checks is insecure and should be avoided."
    )
    conn.add_argument(
        "--verify_tls",
        "--verify-tls",
        nargs=1,
        default="True",
        dest="verify_tls",
        choices=["True", "true", "False", "false"],
        help=help,
    )

    auth = parser.add_argument_group("Credential options")
    help = "Default: 'admin', Prefers env var 'fw_username' if set"
    auth.add_argument(
        "--username",
        nargs="?",
        dest="username",
        default=None,
        help=help,
    )

    passwd = auth.add_mutually_exclusive_group()
    help = "Prefers env var 'fw_password' if set. Cannot be used with '--use-vault'"
    passwd.add_argument(
        "--password",
        nargs="?",
        dest="password",
        default=None,
        help=help,
    )

    help = "Use HashiCorp Vault to retrieve credentials. Cannot be used with '--password'"
    passwd.add_argument("--use-vault", action="store_true", default=False, help=help)

    actions = parser.add_argument_group("Available actions")
    action = actions.add_mutually_exclusive_group()

    help = "Perform a query against collected records"
    action.add_argument("-q", "--query", action="store_true", help=help)

    help = "Execute a single command on one or more firewalls"
    action.add_argument("-c", "--command", action="store_true", help=help)

    help = "Execute script(s) on one or more firewalls"
    action.add_argument("-s", "--script", action="store_true", help=help)

    help = "Run a stored report against collected records"
    action.add_argument("-r", "--report", action="store_true", help=help)

    action.add_argument(
        "-noop", dest="noop", action="store_true", default=False, help=_args.SUPPRESS
    )

    # Added explicitly so it can be passed to action parsers
    help = "show this help message and exit"
    parser.add_argument("-h", "--help", action="store_true", help=help)

    return parser
