""" Object format validation """

from typing import Optional, Any, Sequence, Callable, Union, Set
import datetime

import numpy as np


def is_datetime_formatted_str(s: Any, fmt: str) -> bool:
    """Check that string is date-formatted"""
    if not isinstance(s, str): # possibly redundant, but safer
        return False
    try:
        datetime.datetime.strptime(s, fmt)
        return True
    except Exception as e:
        return False

def is_list_of_strings(obj: Sequence) -> bool:
    """Check that object is a list of strings."""
    return isinstance(obj, list) and all([isinstance(e, str) for e in obj])

def is_list_of_floats(obj: Sequence) -> bool:
    """Check if object is a list of floats."""
    return isinstance(obj, list) and all([isinstance(val, (int, float)) for val in obj])

def is_list_of_list_of_strings(obj: Sequence) -> bool:
    """Check that iterable is a list of lists of strings."""
    return isinstance(obj, list) and all([is_list_of_strings(lst) for lst in obj])

def is_list_of_formatted_strings(obj: Sequence,
                                 fmt_check_func: Callable,
                                 list_len: Optional[int] = None) -> bool:
    """Check that iterable is list of formatted strings (formatting checked by provided function)."""
    if isinstance(obj, list):
        len_cond = True if list_len is None else len(obj) == list_len
        return len_cond and all([fmt_check_func(e) for e in obj])
    return False

def is_list_of_list_of_time_range_strings(obj: Sequence,
                                          func: Callable,
                                          num_ranges: Optional[int] = None) \
        -> bool:
    """Check that object is of the form [[<date_or_timestamp_string>, <date_or_timestamp_string>], ...]."""
    if isinstance(obj, list):
        len_cond = True if num_ranges is None else len(obj) == num_ranges
        return len_cond and all([is_list_of_formatted_strings(lst, func, list_len=2) for lst in obj])
    return False

def is_subset(obj1: Union[Sequence, Set],
              obj2: Union[Sequence, Set]) \
        -> bool:
    """
    Check that the elements in one iterable comprise a subset of the elements in the other.

    For example:
        assert_subset([0, 1, 2], [0, 4, 2, 1]) returns True
        assert_subset([0, 1, 2], [3, 2, 1, 5]) returns False
    """
    return len(set(obj1) - set(obj2)) == 0

def is_list_of_sequences(obj: Sequence,
                         seq_types: tuple,
                         len_: Optional[int] = None) \
        -> bool:
    """
    Check that object is a list of an iterable type (e.g. tuple, list), optionally checking the length of each entry.
    """
    if isinstance(obj, list):
        for e in obj:
            valid = isinstance(e, seq_types) and (True if len_ is None else len(e) == len_)
            if not valid:
                return False
        return True
    return False

def is_dict_of_instances(obj: Sequence,
                         type) \
        -> bool:
    """Check that object is a dict of objects of specified instance(s)."""
    return isinstance(obj, dict) and all([isinstance(val, type) for key, val in obj.items()])

def is_list_of_instances(obj: Sequence,
                         type) \
        -> bool:
    """Check that object is a list of objects of specified instance(s)."""
    return isinstance(obj, list) and all([isinstance(val, type) for val in obj])

def is_int_or_float(val) -> bool:
    return isinstance(val, (int, float, np.int64, np.float64))
