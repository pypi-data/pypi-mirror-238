

from typing import Union, List, Dict, Optional

from .val_utils import is_list_of_strings




def make_sql_query(tablename: str,
                   cols: Optional[List[str]] = None,
                   where: Optional[Dict[str, Union[str, List[str], List[List[str]]]]] = None,
                   limit: Optional[int] = None) \
        -> str:
    """
    Make a basic SQL query.

    WHERE clause entries are specified for conjunction only (e.g. <cond0> AND <cond1> AND ...). Each entry can be
    a single string (for equality condition), a list of strings (for set condition) or a list of 1 length-2 list with
    range endpoints (for datetime ranges).
    """
    assert isinstance(tablename, str)
    assert cols is None or is_list_of_strings(cols)
    assert (where is None or
            all([
                isinstance(val, str) or
                is_list_of_strings(val) or
                (isinstance(val, list) and (len(val) == 1) and is_list_of_strings(val[0]) and (len(val[0]) == 2))
                for val in where.values()
            ])
            )
    assert limit is None or isinstance(limit, int)

    # base query
    if cols is not None:
        keys_str = ','.join(cols)
    else:
        keys_str = '*'
    query = f'SELECT {keys_str} FROM {tablename}'

    # where
    if where is not None:
        where_clauses = []
        for key, val in where.items():
            where_clauses.append(make_sql_query_where_one(tablename, key, val))
        query += ' WHERE' + ' AND '.join(where_clauses)

    # limit
    if limit is not None:
        query += f' LIMIT {limit}'

    return query

def make_sql_query_where_one(tablename: str,
                             key: str,
                             val: str) \
        -> str:
    """Create a single where clause entry"""
    if isinstance(val, str):  # equality
        return f" {tablename}.{key} = '{val}'"
    elif isinstance(val, list):  # range or subset
        if isinstance(val[0], list):  # range
            return f" {tablename}.{key} BETWEEN '{val[0][0]}' AND '{val[0][1]}'"
        else:  # subset
            val_strs = [f"'{s}'" for s in val]  # add apostrophes for SQL query with strings
            return f" {tablename}.{key} IN ({','.join(val_strs)})"
    raise Exception('Where clause options not recognized.')