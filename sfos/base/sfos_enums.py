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

from enum import Enum

# Enum classes


class SfosMode(Enum):
    """Mode constants used in SFOS WebAdmin calls"""

    NONE = 0
    GET_INDEX_JSP = 0
    TEST = 99999
    HOST_ADD = 51
    HOST_UPDATE = 52
    HOST_DELETE = 53
    ADMIN_LOGIN = 151
    SET_BACKUP_SCHEDULE = 182
    READ_RECORD = 300
    manage_page_detail = 301
    DOWNLOAD_BACKUP = 466
    RESTORE_BACKUP = 467
    DEFAULT_ADMIN_PASSWORD_RESET = 487
    DEFAULT_ADMIN_PASSWORD_CHANGE = 479
    GET_SYSTEM_GRAPH = 557
    API_Congiguration = 804
    GET_HA_TYPE = 1284
    HEARTBEAT_STATUS = 1322
    SERVICE_STATUS = 1329
    REMOVE_BACKUP = 2514

    @property
    def code(self) -> str:
        return str(self.value)

    @property
    def id(self) -> str:
        return self.name

    @property
    def __dict__(self) -> dict:
        return {self.name: self.value}

    def __json__(self) -> dict:
        return self.__dict__


class SfosOperation(Enum):
    """Operation constants used in SFOS WebAdmin calls"""

    NONE = 0
    TEST = -99999
    READ_DEVICE_ACCESS_SETTINGS = 480
    HEARTBEAT_STATUS = 1322
    API_Interface_Set = 1659

    @property
    def code(self) -> str:
        return str(self.value)

    @property
    def id(self) -> str:
        return self.name

    @property
    def __dict__(self) -> dict:
        return {self.name: self.value}

    def __json__(self) -> dict:
        return self.__dict__
