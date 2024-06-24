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
import pytest
import shlex

from sfos import agent as _agent


def parser_t1() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("test", allow_abbrev=True)
    parser.add_argument("-t1", action="store_true", default=False)
    parser.add_argument("-t2", action="store_true", default=False)
    parser.add_argument("-t3", action="store_true", default=False)
    return parser


@pytest.mark.parametrize(
    "raw_args,parser",
    [
        ("-t1", parser_t1()),
        ("-t2", parser_t1()),
        ("-t3", parser_t1()),
        ("-t1 -t2", parser_t1()),
        ("-t1 -t3", parser_t1()),
        ("-t2 -t3", parser_t1()),
        ("-t1 -t2 -t3", parser_t1()),
    ],
)
def test_parse_args(raw_args: str, parser: argparse.ArgumentParser) -> None:
    args = shlex.split(raw_args)
    ns = parser.parse_args(args=args)
    print(
        (
            f"t1 in '{raw_args}' -> {"-t1" in raw_args} - ns.t1 == {ns.t1}\n"
            f"t2 in '{raw_args}' -> {"-t2" in raw_args} - ns.t2 == {ns.t3}\n"
            f"t3 in '{raw_args}' -> {"-t3" in raw_args} - ns.t3 == {ns.t3}"
        )
    )
    assert ("-t1" in raw_args) == ns.t1
    assert ("-t2" in raw_args) == ns.t2
    assert ("-t3" in raw_args) == ns.t3


SINGLE_HOST_NOOP = " ".join([
    "--hostname test.fw.name",
    "--port 4444",
    "--self-signed-cert",
    "--username test_user",
    "--password test_pass",
    "-zz"
])

SINGLE_HOST_COMMAND = " ".join([
    "--hostname test.fw.name",
    "--port 4444",
    "--self-signed-cert",
    "--username test_user",
    "--password test_pass",
    "-c",
    "DOWNLOAD_BACKUP"
])

SINGLE_HOST_QUERY = " ".join([
    "--hostname test.fw.name",
    "--port 4444",
    "--self-signed-cert",
    "--username test_user",
    "--password test_pass",
    "-q",
    "serial_number",
    "like",
    "X%"
])


# SINGLE_HOST_COMMAND,
# SINGLE_HOST_QUERY,
@pytest.mark.parametrize(
    "raw_args", [SINGLE_HOST_NOOP],
)
def test_parser_prod(raw_args: str) -> None:
    # parsers = _agent.init_cli()
    args = shlex.split(raw_args)
    result = _agent.read_root_args(args)
    (firewalls, ns, action) = result

    print(firewalls, ns, action)

    assert len(firewalls) == 1
    fw = firewalls[0]

    assert fw.credentials["username"] == "test_user"
    assert fw.credentials["password"] == "test_pass"
    assert fw.address.hostname == "test.fw.name"
    assert fw.address.port == 4444
    assert fw.address.verify_tls is False
    assert action in ["noop", "query", "command",]
