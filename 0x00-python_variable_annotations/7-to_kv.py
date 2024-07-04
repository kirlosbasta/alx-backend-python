#!/usr/bin/env python3
'''7. Complex types - string and int/float to tuple'''
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''return a tuple of k and v squared'''
    return (k, v ** 2)
