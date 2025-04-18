"""SFOS Ground Control
Copyright 2024 Sophos Ltd.  All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
file except in compliance with the License.You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed
to in writing, software distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See
the License for the specific language governing permissions and limitations under the
License.
"""

import json


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

        self.message = json.dumps(kwargs)


class AgentConnectionError(AgentError):
    """Firewall login failed"""


class ConnectionTimeoutError(AgentConnectionError):
    """Firewall login failed"""


class ReadTimeoutError(AgentConnectionError):
    """Firewall connection timed out while reading response"""


class NameResolutionError(AgentConnectionError):
    """Firewall login failed"""


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


class JSONError(ProcessorError):
    """Root error class for all module exceptions"""


class ArgumentError(ProcessorError):
    """Raised when an illogical combination of arguments is provided"""


class ArgumentValueError(ProcessorError):
    """Raised when an arguments value cannot be interpreted"""


class IndexMatchError(ProcessorError):
    """Error matching expected tokens in index.jsp"""


class IndexParserError(ProcessorError):
    """Error parsing index.jsp contents"""


class OperatorError(ProcessorError):
    """Error performing operation"""


class ResponseContentError(ProcessorError):
    """A SfosResponse object does not contain the expected response data"""


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


class DatabaseError(AgentError):
    """A general error for interactions with app database"""
