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
import re as _re

from datetime import datetime
from pydantic import BaseModel
from typing import Literal

from sfos.static import constants as _c, exceptions as _ex, patterns as _p, DATE_FMT


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

    # @property
    # def subscription_list(self) -> list:
    #     result = []
    #     sm = License(self.subscriptions, self.applianceKey)
    #     for this in sm.entitlements:
    #         exp = this.expiry_date.strftime(_DATE_FMT) if this.expiry_date else None
    #         if this.name:
    #             result.append(
    #                 {
    #                     "name": this.name,
    #                     "start": str(this.start_date) if this.start_date else "",
    #                     "end": exp,
    #                     "timeframe": this.expiry_timeframe if exp else "",
    #                 }
    #             )
    #     return result

    # @property
    # def subscription_dict(self) -> dict:
    #     subs = self.subscription_list
    #     result = {sub["name"]: sub for sub in subs if "name" in sub}
    #     return result

    def get_license(self) -> License:
        return License(self.subscriptions, self.applianceKey)


class Entitlement:
    def __init__(self, data, serial_number: str, bundle: str):
        dsta = data.get("Start Date") or ""
        dexp = data.get("Expiry Date") or ""
        self.is_bundle = data.get("is_bundle")
        self.bundle = bundle
        self.serial_number = serial_number
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
    def __dict__(self) -> dict:
        return {
            "serial_number": self.serial_number,
            "name": self.name,
            "start_date": (
                self.start_date.strftime(DATE_FMT) if self.start_date else "NULL"
            ),
            "expiry_date": (
                self.expiry_date.strftime(DATE_FMT) if self.expiry_date else "NULL"
            ),
            "bundle": self.bundle,
            "status": self.status,
            "deactivation_reason": self.deactivation_reason,
            "type": self.subscription_type,
        }

    @property
    def expiry_seconds(self) -> int:
        if self.expiry_date is None:
            return None
        diff = self.expiry_date - datetime.now()
        return diff.total_seconds()

    @property
    def expiry_timeframe(self) -> str:
        return span_desc(self.expiry_seconds)


class License:
    def __init__(self, json_data: str, serial_number: str):
        self.entitlements: list[Entitlement] = []

        try:
            subscriptions_data = json.loads(json_data)
            self.bundle_name = "".join(
                [
                    item["display_bundle"]
                    for item in subscriptions_data
                    if "display_bundle" in item
                ]
            )
            self.entitlements = [
                Entitlement(
                    subscription,
                    bundle=self.bundle_name,
                    serial_number=serial_number,
                )
                for subscription in subscriptions_data
                if "display_bundle" not in subscription
            ]

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)

    def __dict__(self) -> list[dict]:
        return [sub.__dict__ for sub in self.entitlements]


class IndexParser:
    def __init__(self, csrf_key: str = _p.DEFAULT_CSRF_KEY_NAME) -> None:
        """Accepts:
        csrf_key    (Optional) defaults to the static CSRF key value expected
                    at the time of release: "c$rFt0k3n"

        Updates:
            self.csrf_key_name
            self.re_tofind_csrf_key_value
        """
        super().__init__()
        # name of jsp var containing csrf token
        self.csrf_key_name = csrf_key
        self._compile_re_to_find_csrf_key_value()

    def _compile_re_to_find_csrf_key_value(self, csrf_key: str | None = None) -> None:
        """
        updates the self.re_to_find_csrf_value pattern and compiles it
        Accepts:
            csrf_key    (Optional) Key name to use when compiling re_to_find_csrf_value
                        Key name should exclude 'Cyberoam.' prefix
                        If not supplied, self.csrf_key_name is used
        Updates:
            self.re_to_find_csrf_value
        """

        self.csrf_key_name = csrf_key if csrf_key else self.csrf_key_name
        pattern_find_csrf_key_value = (
            f"{_re.escape(self.csrf_key_name)}{_p.PATTERN_PART_FIND_CSRF_VALUE}"
        )
        self.re_to_find_csrf_key_value = _re.compile(pattern_find_csrf_key_value)

    def _search_for_pattern(
        self,
        re_pattern: _re.Pattern[str],
        search_text: str,
        match_group: str | None = None,
    ) -> str:
        """Accepts:
            re_pattern: Pattern[str]    A compiled regex pattern
            search_text: str            A string to search with the compiled pattern
            match_group: str | None     (Optional) A string name of a named match group.
                                        If provided, and the match_group name is present
                                        in the result, then checks search results for a
                                        named capture group matching the supplied name.

        Returns: str
            If a match_group is provided, and found in the results then its value is
            returned as a string.

        Raises:
            px.NoMatchFound    - raised if no match is found or if a match_group is
                              requested but the match_group is not found in the
                              match
        """
        re_match = re_pattern.search(search_text)
        if re_match is None:
            raise _ex.NoMatchFound("No results found")

        if match_group:
            re_found = re_match.group(match_group)
            if re_found is None:
                raise _ex.NoMatchFound("No results found")
            return str(re_found)
        return str(re_match)

    def _find_all_for_pattern(
        self,
        re_pattern: _re.Pattern[str],
        search_text: str,
    ) -> dict:
        """Accepts:
            re_pattern: Pattern[str]    A compiled regex pattern
            search_text: str            A string to search with the compiled pattern

        Returns:
            all discovered keys and values as a dict

        Raises:
            px.NoMatchFound - raised if pattern returns no results
        """
        found_keys = {}

        re_matches = re_pattern.findall(search_text)
        if re_matches is None:
            raise _ex.NoMatchFound(
                "Pattern '{str(re_pattern)}' did not match anything in search_text"
            )

        for re_match in re_matches:
            key: str = str(re_match[0])
            val: str = str(re_match[1])

            found_keys[key] = val
            if len(found_keys) == 0:
                raise _ex.NoMatchFound("Unable to parse index.jsp")
        return found_keys

    def _update_csrf_key_name(self, search_text: str) -> None:
        """Accepts:
            search_text - string value representing response.text reply from sfos
                     index.jsp. Key name may never change, but if it does, this
                     will either prevent an auth failure after a firmware update,
                     or make it faster to identify the reason it does.

        Updates:
            re_csrf_pattern

        Raises:
            px.NoMatchFound - raised if csrf key name cannot be located
        """

        # print(
        #    f"searching index.jsp for csrf key pattern='{str(_v.RE_TO_FIND_CSRF_KEY)}'"
        # )

        csrf_key_name: str | None = None
        try:
            csrf_key_name = self._search_for_pattern(
                _p.RE_TO_FIND_CSRF_KEY,
                search_text,
                "csrf_key",
            )
            self.csrf_key_name = csrf_key_name
            self._compile_re_to_find_csrf_key_value

        except _ex.NoMatchFound as e:

            raise _ex.NoMatchFound() from e

    def _update_and_find_csrf_token_value(
        self,
        search_text: str,
    ) -> None:
        """Accepts:
            search_text: str            A string to search with the compiled pattern

        Returns:
            None
        Updates:
            self.csrf_key_name - calls self._update_csrf_key_name(search_text) first
            self.csrf_token_value - updated with the value found
        Raises
            px.NoMatchFound - raised if no token is found
        """

        try:
            self._update_csrf_key_name(search_text)
            self.csrf_token_value = self._search_for_pattern(
                self.re_to_find_csrf_key_value, search_text, "csrf_value"
            )
        except _ex.NoMatchFound as e:
            raise _ex.NoMatchFound from e

    def _find_subscriptions(self, search_text: str) -> str:
        """Accepts:
            search_text -
        Returns:

        Updates:

        Raises:
        """
        subscriptions = self._search_for_pattern(
            _p.RE_TO_FIND_SUBSCRIPTIONS, search_text, "subscriptions"
        )
        return subscriptions

    def _extract_key_value_pairs(self, search_text: str) -> dict:
        """Accepts:
            search_text - index_jsp text to search for jasp variable definitions

        Returns:
            dict containing key:value pairs

        Raises:
            KeyParsingError - raised if no key/value pairs are found
        """
        found_keys: dict = {}

        matches = _p.RE_TO_FIND_JSP_VARS.findall(search_text)

        for this in matches:
            key: str = str(this[0])
            val: str = str(this[1])
            found_keys[key] = val
            if len(found_keys) == 0:
                raise _ex.KeyParsingError("Unable to parse index.jsp")

        if found_keys == {}:
            raise _ex.NoMatchFound(
                (
                    "No matches found when searching for key value pairs"
                    f" search_text:len='{len(search_text)}'"
                )
            )

        return found_keys

    def _trim(self, search_text: str) -> str:
        """Accepts:
            search_text     text to process
        Returns:
            str             search_text with repetitive fillers removed:
                            * repeated spaces
                            * repeated line breaks
                            * all tabs
        Updates:

        Raises:
        """
        return_value = search_text
        return_value = return_value.replace("\t", " ")
        return_value = return_value.replace("\r\n", "\n")
        return_value = _re.sub("\n+", "\n", return_value, flags=_re.S)
        return_value = _re.sub(" +", " ", return_value)
        return return_value

    def _reduce_html_to_interesting_bits(self, search_text: str) -> str:
        """Accepts:
            search_text     Raw index.jsp contents

        Returns:
            str             Extracted <script>*</script> contents from search_text

        Raises:
            ProcessorError  Raised if no relevant script data is found
        """
        index_scripts = _p.RE_TO_FIND_SCRIPTS.findall(search_text)
        return_text = ""
        for script in index_scripts:
            this = self._trim(str(script))
            # print(f"interesting bits: {this}")
            return_text += this

        if not return_text:
            # print("No data in search_text to parse")
            raise _ex.ProcessorError("No relevant data found in raw_index_text")

        return return_text

    def __call__(self, raw_text: str) -> FirewallInfo:
        """Accessing index.jsp is the final step to sucecssfully authenticate
        a webadmin session. index.jsp contains the csrf token granted
        by successuflly authenticating.

        In addition, it also contains a wealth of interesting information
        about the firewall, including model, serial number, firmware version,
        license info, and more. This method extracts the interesting
        information and returns a dict containing interesting keys/value info

        Accepts:
            raw_index_text   Contents from index_jsp

        Returns:
            FirewallInfo class containing extracted details

        Raises:
            ProcessorError - raise if no searchable script data found in raw_index_text
        """

        try:

            source_text = self._reduce_html_to_interesting_bits(raw_text)
            search_text = raw_text

            # Strip the returned html down to just the <script> tag contents
            # print(f"Starting parser with search_text bytes={len(search_text)}")
            found_items = self._extract_key_value_pairs(search_text)

            if len(found_items) == 0:
                raise _ex.NoMatchFound("'index.jsp' values not in raw_text")

            # print(f"looking for {self.csrf_key_name} in search_text")
            if self.csrf_key_name in found_items:
                # print("csrf key found in dict")
                found_items["csrf_token"] = found_items[self.csrf_key_name]
            else:
                # print("csrf key not found in dict. Starting hunt")
                self._update_and_find_csrf_token_value(search_text)
                found_items["csrf_token"] = self.csrf_token_value

            # Store the raw index text and all found keys in found_items
            found_items["_source_data"] = source_text
            found_items["all_items"] = found_items

            found_items["subscriptions"] = self._find_subscriptions(search_text)

            # Are all required keys present?

            FirewallInfo.check_required_keys(found_items)
            # print(f'action="found {len(found_items)} key-value pairs in search_text')

        except _ex.NoMatchFound as e:
            raise _ex.NoMatchFound(str(e)) from e

        except _ex.KeyMissingError as e:
            raise _ex.KeyMissingError(str(e)) from e

        except _ex.KeyParsingError as e:
            raise _ex.KeyParsingError(str(e)) from e

        except _ex.CSRFTokenError as e:
            raise _ex.CSRFTokenError(str(e)) from e

        # return FirewallInfo created from required_key values
        required_params = FirewallInfo.required_params()
        return_obj_values = {key: found_items[key] for key in required_params}

        # print(
        #     f"type:{type(return_obj_values)}\n"
        #     f" keys:{[key for key in return_obj_values.keys()]}\n"
        #     f" req:{required_params}"
        # )
        result = FirewallInfo()
        for key in return_obj_values:
            setattr(result, key, return_obj_values[key])

        return result


parse_index = IndexParser()


def span_desc(seconds: float | None) -> str:
    if not seconds:
        return ""
    if seconds < 0:
        return "PAST"
    elif seconds < _c.ONEDAY:  # a day
        return "Today"
    elif seconds < _c.ONEDAY * 2:
        return "Tomorrow"
    elif seconds < (_c.ONEWEEK * 2):
        return f"{int(seconds/_c.ONEDAY)} days"
    elif seconds < _c.ONEYEAR:
        return f"{int(seconds/_c.ONEWEEK)} weeks"
    elif seconds < (_c.ONEYEAR * 2):
        return "Over a year"
    else:
        return f"{int(seconds/_c.ONEYEAR)} years"
