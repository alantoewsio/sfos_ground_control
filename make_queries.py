from sfos.db import Select

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
