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

from argparse import ArgumentParser as _ap


def setup_command_arguments(parser: _ap) -> _ap:

    help = "Name of command to run"
    parser.add_argument("command", nargs="?", help=help)

    help = "object data to use with command"
    parser.add_argument(
        "-o", "--object", nargs="?", required=False, dest="object", help=help
    )

    help = "data payload to pass to command"
    parser.add_argument(
        "-d", "--data", nargs="?", required=False, dest="data", help=help
    )

    help = (
        "Saves response to named file. "
        "Contents will be overwritten unless --append is set"
    )
    parser.add_argument(
        "-w",
        "--write_to_file",
        nargs="?",
        required=False,
        help=help,
    )

    help = "Appends response to file. Requires -w"
    parser.add_argument("-a", "--append", action="store_true", help=help)

    help = "Print response to STDOUT"
    parser.add_argument("-p", "--print", action="store_true", help=help)

    return parser
