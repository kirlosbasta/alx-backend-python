#!/usr/bin/env python3
'''1. Async Comprehensions'''
import asyncio
import random
from typing import List


async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    '''return a list of 10 random floats'''
    return [i async for i in async_generator()]
