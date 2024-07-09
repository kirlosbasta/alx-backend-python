#!/usr/bin/env python3
'''2. Run time for four parallel comprehensions'''
import asyncio
import time


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    '''return the time that needed for async_comprehension to run 4 times'''
    start = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end = time.perf_counter() - start
    return end
