import re as _re

# Static REGEX definitions
GROUP_CSRF_KEY_NAME = "csrf_key"
GROUP_CSRF_KEY_VALUE = "csrf_value"
GROUP_JSP_VAR_KEY = "key"
GROUP_JSP_VAR_VALUE = "value"
GROUP_SUBSCRIPTIONS = "subscriptions"
DEFAULT_CSRF_KEY_NAME = "c$rFt0k3n"
PATTERN_FIND_SCRIPTS = r"<script.*?>(?P<script>.*?)<\/script>"

# raw r"setCSRFToken\((?P<csrf_value>.*?)\)"
PATTERN_FIND_CSRF_KEY_NAME = r"setCSRFToken\((?P<" f"{GROUP_CSRF_KEY_NAME}" r">.*?)\)"
PATTERN_PART_FIND_CSRF_VALUE = r"\s=\s'(?P<" f"{GROUP_CSRF_KEY_VALUE}" r">\w+)'"
PATTERN_FIND_CSRF_KEY_VALUE_DEFAULT = (
    f"{_re.escape(DEFAULT_CSRF_KEY_NAME)}{PATTERN_PART_FIND_CSRF_VALUE}"
)

# raw pattern: r"Cyberoam\.(?P<key>.+)\s*=\s*('|\")(?P<value>.*?)(\"|');"
PATTERN_FIND_JSP_VARS = (
    r"Cyberoam\.(?P<"
    f"{GROUP_JSP_VAR_KEY}"
    r">[a-zA-Z0-9!@#$%^&]+)\s*=\s*"
    r"'?\"?(?P<value>.*?)'?\"?;"
)
PATTERN_FIND_SUBSCRIPTIONS = (
    r"modulesubsctionList=(?P<" f"{GROUP_SUBSCRIPTIONS}" r">\[.*\]);"
)

# Compiled static regex patterns
RE_TO_FIND_SCRIPTS = _re.compile(PATTERN_FIND_SCRIPTS, flags=_re.S)
RE_TO_FIND_CSRF_KEY = _re.compile(PATTERN_FIND_CSRF_KEY_NAME)
RE_TO_FIND_JSP_VARS = _re.compile(PATTERN_FIND_JSP_VARS)
RE_TO_FIND_SUBSCRIPTIONS = _re.compile(PATTERN_FIND_SUBSCRIPTIONS)
RE_TO_FIND_CSRF_KEY_VALUE_DEFAULT = _re.compile(PATTERN_FIND_CSRF_KEY_VALUE_DEFAULT)
