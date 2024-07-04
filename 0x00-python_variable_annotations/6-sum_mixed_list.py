#!/usr/bin/env python3
'''6. Complex types - mixed list'''
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''function that takes a list of floats as argument
    and returns their sum'''
    return sum(mxd_lst)
