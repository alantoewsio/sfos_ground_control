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

__all__ = [
    "run_cli_command",
    "run_query",
    "run_scripts",
]

from sfos.agent.actions.command import run_cli_command
from sfos.agent.actions.query import run_query
from sfos.agent.actions.script import run_scripts


def run_noop() -> None:
    """_summary_
    """
    print("No-op executed flawlessly")
