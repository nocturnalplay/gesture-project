#!/usr/bin/env python

import asyncio
from websockets import connect
import sys


async def hello(uri):
    async with connect(uri, ping_interval=None) as websocket:
        await websocket.send("Hello world!")
        while 1:
            print(await websocket.recv())

asyncio.run(hello(f"ws://{sys.argv[1]}:{sys.argv[2]}"))
