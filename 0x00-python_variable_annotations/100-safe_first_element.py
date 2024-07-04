#!/usr/bin/env python3
'''10. Duck typing - first element of a sequence'''
from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''return the first element or none'''
    if lst:
        return lst[0]
    else:
        return None
