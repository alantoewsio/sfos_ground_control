# Database Formats
DATE_FMT = "%Y-%m-%d"
DATE_TIME_FMT = "%Y-%m-%d %H:%M:%S"


ONEHOUR = 60 * 60  # Seconds
ONEDAY = ONEHOUR * 24  # Hours
ONEWEEK = ONEDAY * 7  # Days
ONEMONTH = ONEWEEK * 4  # Weeks
ONEYEAR = ONEDAY * 365  # Days

# Byte math
KB = 1024
MB = KB * 1024
GB = MB * 1024
TB = GB * 1024

# Web request/response key name definitions
USERNAME = "username"
PASSWORD = "password"
CAPTCHA = "captcha"
JSESSIONID = "JSESSIONID"
CSRF_TOKEN = "X-Csrf-Token"
AUTH_SUCCESS_MSG = '{"redirectionURL":"/webpages/index.jsp","status":200}'
AUTH_FAIL_MSG = '{"redirectionURL":"/webpages/login.jsp","status":-1}'
AUTH_DISCLAIMER_MSG = '"disclaimer_message":"'

# Log Formatting
LOG_FORMAT = (
    '%(asctime)s "%(levelname)s" file="%(filename)s" line="%(lineno)s" '
    'func="%(funcName)s()" message="%(message)s"'
)
AGENT_LOG_FORMAT = '%(asctime)s "%(levelname)s" %(message)s'
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
