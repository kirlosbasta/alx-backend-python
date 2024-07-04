#!/usr/bin/env python3
'''8. Complex types - functions'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''return a function that multiply a float'''
    return lambda x: x * multiplier
