import re
from typing import Iterator, Tuple, Optional


def decapitalize(string: str):
    return string[:1].lower() + string[1:]


def concatenate_string(
    iterator: Iterator[str],
    delimiter: str = ", ",
    last_delimiter: str = " et ",
    last_ponctuation="",
) -> str:
    list_it = list(iterator)
    return (
        delimiter.join(list_it[:-1]) + last_delimiter + list_it[-1]
        if len(list_it) > 1
        else f"{list_it[0]}"
    ) + last_ponctuation


def split_var_name(var_name: str) -> Tuple[str, Optional[int], Optional[str]]:
    """Splits a variable name following the pattern <prefix><accum>__<vertical_level>
    into a tuple (<prefix>, <accum>, <vertical_level>).

    Args:
        var_name (str): Variable name

    Returns:
        Tuple[str, Optional[int], Optional[str]]: Tuple containing the:
            - prefix
            - the accumulation value (optional)
            - the vertical level (optional)
    """
    prefix, accum, vert_level = re.match(
        r"^([a-zA-Z_]+)(\d*)__(.*)$", var_name
    ).groups()
    if accum == "":
        accum = 0
    accum = int(accum)
    return prefix, accum, vert_level
