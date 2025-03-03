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

# pylint: disable=broad-exception-caught

import csv
import prettytable
from datetime import datetime
from sfos.base.db import init_db
from sfos.agent.cli_args import read_root_args
from sfos.agent.actions import run_cli_command, run_query, run_scripts
from sfos.logging import (
    Level,
    log,
    logdebug,
    loginfo,
    logerror,
    init_logging,
    # log_callstart,
    # log_calldone,
)

init_logging(level=Level.INFO)
loginfo(action="Starting", task="init_db")
db = init_db()


def write_csv(query: str, filename: str = "output.csv"):
    cursor = db.get_cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = list(map(lambda x: x[0], cursor.description))
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(data)
    logdebug(f"Data written to csv file:{filename}")


def print_table(query: str):
    cursor = db.get_cursor()
    cursor.execute(query)
    # cursor.fetchall()
    table = prettytable.from_db_cursor(cursor)
    print(table)


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
                (r.fw.address.address, r.success, r.error) for r in results
            ]
            loginfo(action="command", results=command_summary)
            if args.command == "refresh":
                # query = "SELECT * FROM inventory_view"
                query = db.load_sql_from_file("dashboard.sql")
                try:
                    now = datetime.now()
                    now.strftime("%Y%m%d-%H-%M-%S")
                    filename = f"refresh_{now.strftime('%Y%m%d-%H-%M-%S')}.csv"
                    logdebug(f"Refresh done. printing results from query: {query}")
                    write_csv(
                        query,
                        filename=filename,
                    )
                    print_table(query)
                    print(f"Results saved to '{filename}'")

                except Exception as e:
                    logerror(e)
                    print(f"Actions complete - error displaying summary. {e}")

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
            print("args", type(args))
            log(
                Level.INFO,
                action="query",
                # args=str(list(args)),  # type:ignore
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
