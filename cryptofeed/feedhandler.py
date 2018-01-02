'''
Copyright (C) 2017-2018  Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import asyncio

import websockets


class FeedHandler(object):
    def __init__(self):
        self.feeds = []
    
    def add_feed(self, feed):
        self.feeds.append(feed)
    
    def run(self):
        asyncio.get_event_loop().run_until_complete(self._run())

    def _run(self):
        loop = asyncio.get_event_loop()
        feeds = [asyncio.ensure_future(self._connect(feed)) for feed in self.feeds]
        done, pending = yield from asyncio.wait(feeds)
    
    async def _connect(self, feed):
        async with websockets.connect(feed.address) as websocket:
            await feed.subscribe(websocket)
            await self._handler(websocket, feed.message_handler)

    async def _handler(self, websocket, handler):
        async for message in websocket:
            await handler(message)
