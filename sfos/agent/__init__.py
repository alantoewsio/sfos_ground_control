"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.

This module provides interpretation of command line options and execution of those
options. It will import other sfos modules but should not import anything outside of
sfos.static
"""

__all__ = [
    "run_cli_command",
    "run_query",
    "init_cli",
    "read_root_args",
    "db",
    "start_agent",
    "Script",
    "ScriptItem",
    "load_script",
    "execute_script",
    "__version__",
]
__version__ = "2025.04.138-pre"

from sfos.agent.actions import run_cli_command, run_query
from sfos.agent.cli_args import init_cli, read_root_args


from sfos.agent.agent_main import db, start_agent
from sfos.agent.script_objs import (
    Script,
    ScriptItem,
    load_script,
    execute_script,
)
