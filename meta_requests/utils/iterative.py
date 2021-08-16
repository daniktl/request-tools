from itertools import chain, combinations
from typing import Iterable


def power_set(iterable: Iterable) -> Iterable:
    iterable_ls = list(iterable)
    return chain.from_iterable(combinations(iterable_ls, s) for s in range(len(iterable_ls) + 1))
