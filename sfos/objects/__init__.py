""" SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.

This module contains objects returned by public functions in module.
 Nothing in this module should reference anything else within sfos.* except stos.static
 """

__all__ = [
    "CustomDict",
    "Boolean",
    "YesOrNo",
    "TrueOrFalse",
    "EnableOrDisable",
    "EnabledOrDisabled",
    "FirewallInfo",
    "Definition",
    "ServiceAddress",
    "SfosRequest",
    "SfosResponse",
    "StripHTML",
]

from sfos.objects.custom_types import (
    CustomDict,
    Boolean,
    YesOrNo,
    TrueOrFalse,
    EnableOrDisable,
    EnabledOrDisabled,
)
from sfos.objects.firewall_info import FirewallInfo
from sfos.objects.req_definition import Definition
from sfos.objects.service_address import ServiceAddress
from sfos.objects.sfos_request import SfosRequest
from sfos.objects.sfos_response import SfosResponse
from sfos.objects.strip_html import StripHTML
