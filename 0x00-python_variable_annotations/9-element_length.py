#!/usr/bin/env python3
'''9. Let's duck type an iterable object'''
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''return a list of tuples of '''
    return [(i, len(i)) for i in lst]
