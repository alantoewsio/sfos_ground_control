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

import argparse as _args
import prettytable

from sfos.base import GroundControlDB as _db
from sfos.logging.logging import Level


def run_query(
    args: _args.Namespace,
    db: _db,
    print_results: bool = True,
) -> list:
    """_summary_

    Args:
        args (_args.Namespace): _description_
        db (_db): _description_
        print_results (bool, optional): _description_. Defaults to True.

    Returns:
        list: _description_
    """
    results = []

    for file in args.filename:
        query = db.load_query(filename=file)

        if print_results:
            records = query.get_cursor()
            table = prettytable.from_db_cursor(records)
            print(table)

        records = query.fetchall()
        results.append(records)

    return results
