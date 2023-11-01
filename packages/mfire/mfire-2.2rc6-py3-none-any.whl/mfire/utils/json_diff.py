"""function made to check the differences between two given json files
    and highlighting the differences if needed.
"""

import json
from pathlib import Path

from mfire.utils.dict_utils import dict_diff


def json_diff(left: Path, right: Path, verbose: int = 2, **kwargs) -> bool:
    """function made to check the differences between two given json files
    and highlighting the differences if needed.

    Args:
        left (Path): Path to a json file
        right (Path): Path to a json file
        verbose (int, optional): Level of description of the differences.
            Defaults to 2.

    Returns:
        bool: [description]
    """
    with open(left) as lfp:
        left_dico = json.load(lfp)

    with open(right) as rfp:
        right_dico = json.load(rfp)

    return dict_diff(
        left=left_dico,
        right=right_dico,
        index_list="",
        verbose=verbose,
        **kwargs,
    )
