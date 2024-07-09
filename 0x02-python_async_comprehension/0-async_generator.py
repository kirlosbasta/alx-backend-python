#!/usr/bin/env python3
'''0. Async Generator'''
import asyncio
import random
from typing import AsyncIterator


async def async_generator() -> AsyncIterator[float]:
    for i in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
