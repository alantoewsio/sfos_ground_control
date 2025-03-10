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

import sys
import dotenv

from sfos import __version__ as _WorkerVersion
from sfos import agent as _agent
from sfos.logging import agent_loginfo, logerror

dotenv.load_dotenv()


def is_running_as_exe():
    return getattr(sys, "frozen", False) or "__file__" not in globals()


def main() -> None:
    agent_loginfo(
        f"SFOS Ground Control Agent ( {'exe' if is_running_as_exe() else 'py'} version '{_agent.__version__}', worker version '{_WorkerVersion}') starting"
    )
    message = "SFOS Ground Control Agent exiting"
    try:
        _agent.start_agent()
        agent_loginfo(message + " successfully")
        return 0
    except _agent.methods.AgentMethodsError as e:
        message += f"SFOS Ground Control Agent exiting - error(2): {e}"
        agent_loginfo(message)
        print(message)
        return 1
    except:  # noqa: E722 Exempt linting error
        # logging errors should not block application success
        e = sys.exc_info()[0]
        message += f" - Unexpected error(999) {e}"
        logerror(e)
        agent_loginfo(message)
        print(message)
        return 999


if __name__ == "__main__":
    sys.exit(main())
