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

from sfos.base.db import GroundControlDB as _db
from sfos.base.db import instance
from sfos.logging.logging import log, Level
from sfos.static import DATE_TIME_FMT as _DATE_FMT


def init_db(filename: str | None = None) -> _db:
    """Ensure the database file exists, and that it is properly initialized

    Args:
        filename (str | None, optional): _description_. Defaults to None.

    Returns:
        _db: _description_
    """
    instance.db = None
    if filename:
        log(Level.INFO, f"Initializing db '{filename}'")
        instance.db = _db(filename)
    else:
        instance.db = _db()
        log(Level.INFO, f"Initialized db '{instance.db.filename}'")
    assert instance.db  # GroundControlDB class is instantiated successfully
    init_scripts = ["init_tables.sql", "init_views.sql", "init_views.sql"]
    init_scripts_sql = [instance.db.load_sql_from_file("init_tables.sql")]

    if instance.db.create_db(init_scripts_sql):
        log(
            Level.INFO,
            action="init_db",
            files=init_scripts,
            database=instance.db.filename,
        )

    return instance.db
