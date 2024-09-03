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
# pylint: disable=broad-exception-caught

import prettytable
from sfos.base.db import init_db
from sfos.agent.cli_args import read_root_args
from sfos.agent.actions import run_cli_command, run_query, run_scripts
from sfos.logging import (
    Level,
    log,
    loginfo,
    logerror,
    # log_callstart,
    # log_calldone,
)


db = init_db()


def start_agent() -> None:
    """Starts an agent run"""
    # log_callstart(verbose=True)
    firewalls, args, action, rest = read_root_args()  # type: ignore

    match action:
        case "command":
            loginfo(
                action="command",
                args=str(args),
                rest=str(args),
                target_count=len(firewalls),
            )

            results = run_cli_command(firewalls, args, rest, db)
            command_summary = [
                (r.fw.address.address, r.success, r.error) for r in results  # type: ignore
            ]
            loginfo(action="command", results=command_summary)
            if args.command == "refresh":
                query = "SELECT * FROM inventory_dashboard"  # db.load_sql_from_file("dashboard.sql")
                try:
                    records = db.execute(query) if query else []
                    print(f"query 'dashboard.sql' has {len(records)}records")
                    table = prettytable.from_db_cursor(records)
                    print(table)
                except Exception as e:
                    logerror(e)
                    print("Actopns complete - error displaying summary.")

            failures = []
            for sr in results:
                if not sr.success:
                    failures.append(sr)
                    logerror(sr.error)
                    break

            print(
                (
                    f"'{args.command}' attempted on {len(results)} firewalls with "
                    f"{len(failures)} error(s)."
                )
            )

            log(
                Level.INFO,
                action="script",
                result_count=len(results),
                fail_count=len(failures),
                failed_fws=failures,
            )

        case "script":
            log(
                Level.INFO,
                action="script",
                args=str(list(args)),  # type:ignore
                target_count=len(firewalls),
            )
            results = run_scripts(firewalls, args)
            log(Level.INFO, action="script", result_count=len(results))

        case "query":
            log(
                Level.INFO,
                action="query",
                args=str(list(args)),  # type:ignore
                target_count=len(firewalls),
            )
            results = run_query(args=args, db=db)
            log(Level.INFO, action="query", result_count=len(results))

        case "noop":
            log(action="noop", args=str(args), target_count=len(firewalls))
            print("No-op completed successfully")

        case "help":
            # Information only. Help message is displayed by read_root_args()
            log(action="help", args=str(args))
    # log_calldone(verbose=True)
