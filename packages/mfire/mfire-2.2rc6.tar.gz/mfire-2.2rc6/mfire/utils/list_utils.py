from itertools import combinations
from typing import Generator, List, Tuple


def combinations_and_remaining(
    list: List, r: int
) -> Generator[Tuple[List, List], None, None]:
    """
    Generates all combinations and remaining elements of a list. First element is the
    generated element of size r and the second element is the remaining elements.
    """
    for c in combinations(list, r=r):
        diff = [i for i in list if i not in c]
        yield c, diff


def all_combinations_and_remaining(
    list: List, is_symmetric: bool = False
) -> Generator[Tuple[List, List], None, None]:
    """
    Generates all combinations and remaining elements of a list.
    If argument is_symmetric is True then we only generate (combi, remaining) and
    not (remaining, combi) except for list of even size and r=len(list)/2.
    """
    r_max = len(list) // 2 if is_symmetric else len(list)
    for r in range(r_max):
        yield from combinations_and_remaining(list, r + 1)
