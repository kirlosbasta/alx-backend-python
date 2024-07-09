#!/usr/bin/env python3
'''4-tasks'''
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''return a list of n delay times concurrently'''
    tasks = [task_wait_random(max_delay) for i in range(n)]
    res = []
    for future in asyncio.as_completed(tasks):
        result = await future
        res.append(result)
    return res
