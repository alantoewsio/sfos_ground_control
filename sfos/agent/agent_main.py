from sfos.base.db import init_db
from sfos.agent.cli_args import read_root_args
from sfos.agent.actions import run_command, run_query, run_scripts
from sfos.logging.logging import trace_calls, Level, log


db = init_db()


@trace_calls(Level.INFO, False, False)
def start_agent() -> None:
    firewalls, args, action, rest = read_root_args()

    match action:
        case "command":
            log(
                Level.INFO,
                action="command",
                args=str(args),
                rest=str(args),
                target_count=len(firewalls),
            )
            results = run_command(firewalls, args, rest, db)

            failures = []
            for srs in results:

                for sr in srs:
                    if not sr.success:
                        failures.append(sr)
                        print(sr.error)
                        break
                    else:
                        pass
                        # print(sr.text)

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
                failed_fws=str(failures),
            )

        case "script":
            log(
                Level.INFO,
                action="script",
                args=str(list(args)),
                target_count=len(firewalls),
            )
            results = run_scripts(firewalls, args)
            log(Level.INFO, action="script", result_count=len(results))

        case "query":
            log(
                Level.INFO,
                action="query",
                args=str(list(args)),
                target_count=len(firewalls),
            )
            results = run_query(args=args, db=db)
            log(Level.INFO, action="query", result_count=len(results))

        case "noop":
            log(action="noop", args=str(args), target_count=len(firewalls))
            print("No-op completed successfully")

        case "help":
            log(action="help", args=str(args))
            """Information only. Help message is
            displayed by read_root_args()
            """
