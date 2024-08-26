from sfos.db import Select
from sfos.static import DATE_TIME_FMT as _DATE_TIME_FMT

# Create new JSON format queries following the example below,
# then run 'python custom_queries.py' to create query json files.
# example:
query = Select(
    "SUBSTRING(version, 1, 4) as major_ver",
    "MAX(version) as latest",
    from_table="inventory",
    limit=2,
)
query = query.where("version", "is not", None)
query.export("queries/newest_running_firmware.json")

query = (
    Select(
        "companyName",
        "model",
        "count(serial_number) as firewalls",
        "MIN(version) as oldest_version",
        from_table="inventory",
    )
    .group_by("companyName")
    .order_by("companyName")
)
query.export("queries/oldest_firmware_by_company.json")

query = (
    Select(
        "address as Address",
        "serial_number as 'Serial Number'",
        "model as Model",
        "displayVersion as Version",
        "companyName as Company",
        "message as 'Error Message'",
        "last_result as Status",
        f"strftime('{_DATE_TIME_FMT}', last_seen) as 'Last Seen Date' ",
        (
            "CAST ("
            "strftime('%j',current_timestamp) - "
            "strftime('%j',last_seen) "
            "AS INT) as 'Days Ago' "
        ),
        from_table="inventory",
    )
    .order_by("'Last Seen Date'", ascending=False, nulls_first=False)
    .order_by("Status")
)
query.export("queries/status.json")
