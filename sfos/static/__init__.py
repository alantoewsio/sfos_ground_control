""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.

This module contains static values and definitions that may safely be imported by any
module. Nothing in this module should reference anything else within sfos.*"""

__all__ = [
    "QueryOperators",
    "QuerySources",
    "DATE_FMT",
    "DATE_TIME_FMT",
    "Level",
    "SfosMode",
    "SfosOperation",
    "AgentError",
    "ConnectionError",
    "ProcessorError",
]

from sfos.static.aliases import QueryOperators, QuerySources
from sfos.static.constants import DATE_FMT, DATE_TIME_FMT
from sfos.static.enums import Level, SfosMode, SfosOperation
from sfos.static.exceptions import AgentError, ConnectionError, ProcessorError
