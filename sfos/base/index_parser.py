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

import re

from sfos.base import index_match_values as _v, exceptions as px
from sfos.base.firewall_info import FirewallInfo

# from sfos.base.logs import log as # print, log_error as _log_error


class IndexParser:

    def __init__(self, csrf_key: str = _v.DEFAULT_CSRF_KEY_NAME) -> None:
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
            f"{re.escape(self.csrf_key_name)}{_v.PATTERN_PART_FIND_CSRF_VALUE}"
        )
        self.re_to_find_csrf_key_value = re.compile(pattern_find_csrf_key_value)

    def _search_for_pattern(
        self,
        re_pattern: re.Pattern[str],
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
            raise px.NoMatchFound("No results found")

        if match_group:
            re_found = re_match.group(match_group)
            if re_found is None:
                raise px.NoMatchFound("No results found")
            return str(re_found)
        return str(re_match)

    def _find_all_for_pattern(
        self,
        re_pattern: re.Pattern[str],
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
            raise px.NoMatchFound(
                "Pattern '{str(re_pattern)}' did not match anything in search_text"
            )

        for re_match in re_matches:
            key: str = str(re_match[0])
            val: str = str(re_match[1])

            found_keys[key] = val
            if len(found_keys) == 0:
                raise px.NoMatchFound("Unable to parse index.jsp")
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
                _v.RE_TO_FIND_CSRF_KEY,
                search_text,
                "csrf_key",
            )
            self.csrf_key_name = csrf_key_name
            self._compile_re_to_find_csrf_key_value

        except px.NoMatchFound as e:

            raise px.NoMatchFound() from e

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
        except px.NoMatchFound as e:
            raise px.NoMatchFound from e

    def _find_subscriptions(self, search_text: str) -> str:
        """Accepts:
            search_text -
        Returns:

        Updates:

        Raises:
        """
        subscriptions = self._search_for_pattern(
            _v.RE_TO_FIND_SUBSCRIPTIONS, search_text, "subscriptions"
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

        matches = _v.RE_TO_FIND_JSP_VARS.findall(search_text)

        for this in matches:
            key: str = str(this[0])
            val: str = str(this[1])
            found_keys[key] = val
            if len(found_keys) == 0:
                raise px.KeyParsingError("Unable to parse index.jsp")

        if found_keys == {}:
            raise px.NoMatchFound(
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
        return_value = re.sub("\n+", "\n", return_value, flags=re.S)
        return_value = re.sub(" +", " ", return_value)
        return return_value

    def _reduce_html_to_interesting_bits(self, search_text: str) -> str:
        """Accepts:
            search_text     Raw index.jsp contents

        Returns:
            str             Extracted <script>*</script> contents from search_text

        Raises:
            ProcessorError  Raised if no relevant script data is found
        """
        index_scripts = _v.RE_TO_FIND_SCRIPTS.findall(search_text)
        return_text = ""
        for script in index_scripts:
            this = self._trim(str(script))
            # print(f"interesting bits: {this}")
            return_text += this

        if not return_text:
            # print("No data in search_text to parse")
            raise px.ProcessorError("No relevant data found in raw_index_text")

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
                raise px.NoMatchFound("'index.jsp' values not in raw_text")

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

        except px.NoMatchFound as e:
            raise px.NoMatchFound(str(e)) from e

        except px.KeyMissingError as e:
            raise px.KeyMissingError(str(e)) from e

        except px.KeyParsingError as e:
            raise px.KeyParsingError(str(e)) from e

        except px.CSRFTokenError as e:
            raise px.CSRFTokenError(str(e)) from e

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
