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

from pathlib import Path
from sqlite3 import Connection
import pandas as pd
from sfos.logging import logdebug


def load_query_from_file(
    filename: str, path: str = "sfos/gui/queries/", default: str = None
) -> str:
    """Retrieve the sql found in the given filename or return default if not found

    Args:
        filename (str): _description_
        path (str, optional): _description_. Defaults to "sfos/gui/queries/".
        default (str, optional): _description_. Defaults to None.

    Returns:
        str: contents of sql file
    """
    path = "" if not path else path
    path = f"{path}/" if path and not path.endswith("/") else path
    filename = filename if filename.endswith(".sql") else f"{filename}.sql"
    qfile = Path(path, filename)
    if qfile.exists():
        result = qfile.read_text(encoding="utf-8")
    else:
        result = default

    logdebug(file=qfile,result=result)
    return result


def run_query(
    sql: str,
    connection: Connection,
    *where_filters: str,
    params:list[str]=None,
    index_cols:list[str]=None,
) -> pd.DataFrame:
    """Run a query and return the results in a pd.DataFrame

    Args:
        sql (str): SQL query to exeucte (SQLite)
        connection (sqlite3.Connection): Connection to sqlite database
        where_filter (str, optional): queried as:
          "SELECT * FROM ({sql}) WHERE {where_filter};" if set. Defaults to None.

    Returns:
        pd.DataFrame: Query results as a pandas DatFrame
    """

    where_sql = f" WHERE {" AND ".join(where_filters)}" if where_filters else ""
    full_query = f"SELECT * FROM ({sql}){where_sql}" if where_filters else sql
    return pd.read_sql_query(full_query, connection,params=params,index_col=index_cols)


def run_query_file(
        filename: str,
        *where_filters: str,
        path:str = "sofs/gui/queries/",
        connection:Connection=None,
) -> pd.DataFrame: 
    """Load SQL File 

    Args:
        filename (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    sql = load_query_from_file(filename,path)
    return run_query(sql, connection, *where_filters)
