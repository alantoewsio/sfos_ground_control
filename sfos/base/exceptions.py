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

import json
import re

from html.parser import HTMLParser as _html_parser
from io import StringIO as _string_io


class AgentError(Exception):
    """Root error class for all exceptions raised by this application"""

    def __init__(
        self,
        *args: str | int | list,
        **kwargs: str | int | list,
    ) -> None:
        message: str | None = None
        if args:
            message = " ".join([str(arg) for arg in args])

        if message and "message" in kwargs:
            message = message + " " + str(kwargs["message"])

        if not message:
            message = ""
        kwargs["message"] = message

        if "html" in kwargs:
            kwargs["html"] = _html_stripper(kwargs["html"])

        self.message = json.dumps(kwargs)


class CertificateError(AgentError):
    """Firewall certificate failed verification"""


class LoginError(AgentError):
    """Firewall login failed"""


class LoginCaptchaError(AgentError):
    """Firewall is requestiong a captcha be filled"""


class LoginTosError(AgentError):
    """Firewall is asking user to approve TOS"""


class InvalidParameter(AgentError):
    """Method parameter is an invalid type or content"""


class ProcessorError(AgentError):
    """Root error class for all module exceptions"""


class ArgumentValueError(ProcessorError):
    """Raised when an arguments value cannot be interpreted"""


class IndexMatchError(ProcessorError):
    pass


class IndexParserError(ProcessorError):
    pass


class OperatorError(ProcessorError):
    pass


class NoMatchFound(ProcessorError):
    """Error indicates that response text does not match expected contents
    and was not successfully parsed"""


class CSRFTokenError(ProcessorError):
    """Indicates that a CSRF token was not successfully retrieved"""


class PropertyNotSetError(ProcessorError):
    """Indicates that expected key values were not found"""


class KeyMissingError(ProcessorError):
    """Indicates that expected key values were not found"""


class KeyParsingError(ProcessorError):
    """Indicates that expected key values were not found"""


class NotConfigured(ProcessorError):
    """Indicates that a class is missing parameters to call a method"""


class DefinitionNotFound(AgentError):
    """Definition file cannot be found in specified paths"""


#########################################


class StripHTML(_html_parser):
    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = _string_io()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

    def strip(self, html: str | int | list) -> str:
        self.feed(str(html))

        stripped = self.get_data()
        return stripped

    def abbreviate(self, text: str, max_len: int | None = 100) -> str:
        # replace line breaks and tabs with spaces
        text = text.replace("\r", " ")
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        # remove repetitive spaces
        text = re.sub(r" +", " ", text)
        if max_len:
            text = text[:max_len]
        return text

    def __call__(self, html: str | int | list, max_len: int = 100) -> str:
        result = self.strip(html)
        result = self.abbreviate(result, max_len)
        return result


_html_stripper = StripHTML()
