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


def setup_root_arguments(parser: _ap) -> _ap:
    """Define root cli arguments

    Args:
        parser (_ap): _description_
    """
    # print("Setting up root cli arguments")
    # Added explicitly so it can be passed to action parsers
    help = "show this help message and exit"
    parser.add_argument("-h", "--help", action="store_true", help=help)

    help = "IP or Hostname of SFOS firewall"
    parser.add_argument("--hostname", nargs="?", dest="hostname", help=help)

    help = "WebAdmin port (1-65535)"
    parser.add_argument("--port", type=int, default=4444, dest="port", help=help)

    help = "Required if firewall is using self-signed certificate"
    parser.add_argument(
        "--self-signed-cert",
        default=True,
        action="store_false",
        dest="verify_tls",
        help=help,
    )
    help = "Will use environment var FW_USERNAME if omitted"
    parser.add_argument("--username", nargs="?", dest="username", help=help)

    help = "Will use environment var FW_PASSWORD if omitted (RECOMMENDED)"
    parser.add_argument("--password", nargs="?", dest="password", help=help)

    help = (
        "Inventory list of firewalls to act on - will use --username, --password and "
        "--port arguments if omitted from inventory record"
    )
    parser.add_argument("-i", "--inventory-file", dest="inventory", help=help)

    help = (
        "Use HashiCorp Vault to retrieve credentials - will supersede --password value"
    )
    parser.add_argument("--use-vault", action="store_true", default=False, help=help)

    action = parser.add_mutually_exclusive_group()

    help = "Perform a query against collected records"
    action.add_argument("-q", "--query", action="store_true", help=help)

    help = "Execute a single command on one or more firewalls"
    action.add_argument("-c", "--command", action="store_true", help=help)

    help = "Execute script(s) on one or more firewalls"
    action.add_argument("-s", "--script", action="store_true", help=help)

    help = "Run a stored report against collected records"
    action.add_argument("-r", "--report", action="store_true", help=help)

    help = argparse.SUPPRESS
    action.add_argument(
        "-zz", dest="noop", action="store_true", default=False, help=help
    )

    return parser
