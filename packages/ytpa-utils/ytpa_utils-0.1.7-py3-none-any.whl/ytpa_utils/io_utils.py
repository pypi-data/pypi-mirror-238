

import json
from typing import Union, List






""" Input-output """
def save_json(path: str,
              obj: Union[List[dict], dict],
              mode: str = 'w'):
    """Save object to JSON-formatted file."""
    with open(path, mode) as fp:
        json.dump(obj, fp, indent=4)

def load_json(fpath: str) -> Union[dict, list]:
    """Load from JSON-formatted file"""
    with open(fpath, 'r') as fp:
        return json.load(fp)