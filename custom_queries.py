from sfos.db import Select

# Create new JSON format queries following the example below,
# then run 'python custom_queries.py' to create query json files.
# example:
query = Select(from_table="fwinfo_latest").where("version", "is", None)
query.export("unsuccessful_hosts.JSON")
