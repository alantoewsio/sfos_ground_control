from colorama import Fore  # , Back, Style

from sfos.agent.init_db import init_db
from sfos.agent.cli_args import read_root_args
from sfos.agent.actions import run_command, run_query, run_scripts
from sfos.webadmin.connector import SfosResponse as _sresp

db = init_db()


def print_column_names(sresp: _sresp) -> None:
    if isinstance(sresp.data, dict):
        cols = "| Firewall |"
        for k in sresp.data:
            cols += f" {k} |"
        print(Fore.BLUE + cols + Fore.WHITE)


def print_column_data(sresp: _sresp) -> None:
    if isinstance(sresp.data, dict):
        cols = f" {sresp.fw.address.hostname} |"
        for k, v in sresp.data.items():
            cols += f" {v} |"
        print("|" + cols)


def start_agent() -> None:
    firewalls, args, action = read_root_args()
    match action:
        case "command":
            results = run_command(firewalls, args, db)
            error_count = len([sr for sr in results if not sr.success])
            print(
                (
                    f"'{args.command}' attempted on {len(results)} firewalls with "
                    f"{error_count} errors."
                )
            )

        case "query":
            print("running query", args)
            results = run_query(args=args, db=db)

        case "report":
            pass
        case "script":
            results = run_scripts(firewalls, args)

        case "noop":
            print("No-op executed flawlessly")

        case "help":
            """Information only. Help message is
            displayed by read_root_args()
            """
