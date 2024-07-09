#!/usr/bin/env python3
'''1. Let's execute multiple coroutines at the same time with async'''
import asyncio
from typing import List
import random


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''return a list of n delay times concurrently'''
    tasks = [wait_random(max_delay) for i in range(n)]
    res = []
    for future in asyncio.as_completed(tasks):
        result = await future
        res.append(result)
    return res
