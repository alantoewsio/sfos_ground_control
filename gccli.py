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

from sfos import agent as _agent

DATE_FMT = "%Y-%m-%d"


def main() -> None:
    db = _agent.init_db()
    firewalls, args, action = _agent.read_root_args()
    match action:
        case "command":
            results = _agent.run_command(firewalls, args, db)
            print(f"Done. {len(results)} results stored in db results:\n", results)

        case "query":

            pass
        case "report":
            pass
        case "script":
            pass
        case "noop":
            print("No-op executed flawlessly")

        case "help":
            """Information only. Help message is
            displayed by read_root_args()
            """


if __name__ == "__main__":
    exit(main())
