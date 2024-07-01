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

from __future__ import annotations
import json
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

from sfos.base import exceptions as _ex


class FirewallInfo(BaseModel):
    csrf_token: str | None = None
    displayModel: str | None = None
    displayVersion: str | None = None
    version: str | None = None
    subscriptions: str | None = None
    applianceKey: str | None = None
    isOEMdevice: str | None = None
    loginUserName: str | None = None
    name: str | None = None
    companyName: str | None = None
    disableAdmin: str | None = None
    deviceProperty: str | None = None
    start: str | None = None
    all_items: dict | None = None
    _source_data: str | None = None

    @staticmethod
    def required_params() -> list[str]:
        """Returns:
        list[str] containing FirewallInfo parameter names
        """
        # Get a list of keys needed by FirewallInfo
        result = [key for key in FirewallInfo.model_fields.keys()]
        return result

    @staticmethod
    def check_required_keys(v: dict) -> Literal[True]:
        """Accepts:
            v: dict
        Returns:
            True - if v contains all parameter keys required by FirewallInfo
        Raises:
            KeyMissingError If any required keys are not present in v.
        """
        v_keys = set(v.keys())
        req_keys = set(FirewallInfo.required_params())
        missing = req_keys - v_keys
        if len(missing) > 0:
            raise _ex.KeyMissingError(f"Missing keys {missing}\nFound keys:{v_keys}")
        return True

    @property
    def base_info(self) -> dict:
        return {
            "Model": self.displayModel,
            "displayVersion": self.displayVersion,
            "version": self.version,
            "serial_number": self.applianceKey,
            "companyName": self.companyName,
            "username": self.name,
        }

    def to_json(self, indent: Literal[0, 1, 2, 3, 4] = 2) -> str:
        return json.dumps(self.base_info, indent=indent)

    @property
    def subscription_list(self) -> list:
        result = []
        sm = SubscriptionManager(self.subscriptions)
        for this in sm.subscriptions:
            exp = this.expiry_date.strftime(DATE_FMT) if this.expiry_date else None
            if this.name:
                result.append(
                    {
                        "name": this.name,
                        "start": str(this.start_date) if this.start_date else "",
                        "end": exp,
                        "timeframe": this.expiry_timeframe if exp else "",
                    }
                )
        return result

    @property
    def subscription_dict(self) -> dict:
        subs = self.subscription_list
        result = {"license_" + sub["name"]: sub for sub in subs if "name" in sub}
        return result

    def license(self) -> SubscriptionManager:
        return SubscriptionManager(self.subscriptions)


DATE_FMT = "%Y-%m-%d"
ONEHOUR = 60 * 60
ONEDAY = ONEHOUR * 24
ONEWEEK = ONEDAY * 7
ONEMONTH = ONEWEEK * 4
ONEYEAR = ONEDAY * 365


def span_desc(seconds: float | None) -> str:
    if not seconds:
        return ""
    if seconds < 0:
        return "PAST"
    elif seconds < ONEDAY:  # a day
        return "Today"
    elif seconds < ONEDAY * 2:
        return "Tomorrow"
    elif seconds < (ONEWEEK * 2):
        return f"{int(seconds/ONEDAY)} days"
    elif seconds < ONEYEAR:
        return f"{int(seconds/ONEWEEK)} weeks"
    elif seconds < (ONEYEAR * 2):
        return "Over a year"
    else:
        return f"{int(seconds/ONEYEAR)} years"


class Subscription:
    def __init__(self, data):
        dsta = data.get("Start Date") or ""
        dexp = data.get("Expiry Date") or ""
        self.is_bundle = data.get("is_bundle")
        self.status = data.get("Status")
        self.deactivation_reason = data.get("deactivation_reason")
        self.subscription_type = data.get("Type")
        self.start_date = (
            None if dsta in ["", "null"] else datetime.strptime(dsta, DATE_FMT)
        )
        self.expiry_date = (
            None if dexp in ["", "null"] else datetime.strptime(dexp, DATE_FMT)
        )
        self.name = data.get("Name")

    @property
    def expiry_seconds(self) -> int:
        if self.expiry_date is None:
            return None
        diff = self.expiry_date - datetime.now()
        return diff.total_seconds()

    @property
    def expiry_timeframe(self) -> str:
        return span_desc(self.expiry_seconds)


class SubscriptionManager:
    def __init__(self, json_data):
        self.subscriptions: Subscription = []
        self.parse_json(json_data)

    def parse_json(self, json_data):
        try:
            subscriptions_data = json.loads(json_data)
            bundle = []
            alacarte = []
            for subscription in subscriptions_data:
                this_sub = Subscription(subscription)
                if this_sub.name is None:
                    break
                if this_sub.is_bundle:
                    bundle.append(this_sub)
                else:
                    alacarte.append(this_sub)

            self.subscriptions.extend(bundle)
            self.subscriptions.extend(alacarte)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
