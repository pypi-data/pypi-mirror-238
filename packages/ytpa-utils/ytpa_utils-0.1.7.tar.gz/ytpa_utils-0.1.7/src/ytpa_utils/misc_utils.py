"""Miscellaneous utils"""

import re
from typing import Union, List, Optional, Tuple
import time
from PIL import Image
import requests
import io

import pandas as pd




""" Other """
def convert_num_str_to_int(s: str) -> int:
    """
    Convert number strings to integers. Assumes resulting number is an integer. Handles strings of the form:
    - 535
    - 54,394
    - 52.3K
    - 3.8M
    - 40M
    """
    if s == '':
        return 0
    s = s.replace(',', '')
    if 'K' in s:
        s = int(float(s[:-1]) * 1e3)
    elif 'M' in s:
        s = int(float(s[:-1]) * 1e6)
    num = int(s)
    return num

def apply_regex(s: str,
                regex: str,
                dtype: Optional[str] = None) \
        -> Union[List[Tuple[str]], str, int]:
    """
    Apply regex to string to extract a string. Can handle further parsing if string is a number.
    Assumes regex is specified as string with embedded (.*?) to find substring.
    Handles commas separating sequences of digits (e.g. 12,473).
    """
    substring_flag = '(.*?)'
    assert substring_flag in regex
    res = re.findall(regex, s)
    # print(res)
    num_substrings = sum([regex[i:i + len(substring_flag)] == substring_flag for i in range(len(regex) - len(substring_flag))])
    if num_substrings > 1:
        return res
    if len(res) == 0:
        substring = ''
    else:
        substring = res[0]
    # print(substring)
    if dtype == 'int':
        return convert_num_str_to_int(substring)
    return substring

def print_df_full(df: pd.DataFrame,
                  row_lims: Optional[List[int]] = None):
    """Print all rows and columns of a dataframe"""
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.expand_frame_repr', False):
        if row_lims is None:
            print(df)
        else:
            print(df[row_lims[0]:row_lims[1]])

def fetch_data_at_url(url: str,
                      delay: float = 0) \
        -> bytes:
    """Fetch raw_data at specified URL"""
    if delay > 0:
        time.sleep(delay)
    return requests.get(url).content

def convert_bytes_to_image(image_data: bytes) -> Image:
    """Convert byte string to Image"""
    return Image.open(io.BytesIO(image_data))

def remove_trailing_chars(s: str,
                          trail_chars: Optional[List[str]] = None) \
        -> str:
    """Remove trailing chars from a string (e.g. newlines, empty spaces)."""
    if len(s) == 0:
        return s
    if trail_chars is None:
        trail_chars = ['\n', ' ']
    i = len(s) - 1
    while (i >= 0) and (s[i] in trail_chars):
        i -= 1
    return s[:i + 1]

def just_dict_keys(obj: dict) -> Union[dict, None]:
    """Return dictionary with only keys. Leaf values will be replaced with None."""
    if not isinstance(obj, dict):
        return None

    obj_keys = {}
    for key, val in obj.items():
        obj_keys[key] = just_dict_keys(val)

    return obj_keys

