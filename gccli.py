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

from sfos import agent as _agent

dotenv.load_dotenv()


def main() -> None:
    print(f"SFOS Ground Control Agent (version '{_agent.__version__}')")
    try:
        _agent.start_agent()
        return 0
    except KeyError as e:
        print(f"Key error: {e}")
        return 1
    except _agent.methods.AgentMethodsError as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
