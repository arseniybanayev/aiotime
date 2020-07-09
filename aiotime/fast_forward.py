import asyncio
import typing
import functools

class FastForward:
    """
    Takes over the supplied event loop and allows manually moving its internal clock
    forward, for control over methods like `asyncio.sleep`, `loop.call_at` or
    `loop.call_later`.
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        if self._get_next_scheduled_time() is not None:
            raise ValueError('Cannot take over the loop if tasks are already scheduled')
    
    def __enter__(self, *args, **kwargs):
        self._old_time = self.loop.time
        self._time = 0
        self.loop.time = functools.wraps(self.loop.time)(lambda: self._time)
        return self
    
    def __exit__(self, *args, **kwargs):
        self.loop.time = self._old_time

    async def __call__(self, seconds: typing.Union[float, int]):
        if seconds < 0:
            raise ValueError('This is FastForward, not Rewind (seconds must be positive')

        await self._flush()

        # move forward according to what has already been scheduled, until `seconds` later
        end_time = self._time + seconds
        while True:
            next_time = self._get_next_scheduled_time()
            if next_time is None or next_time > end_time:
                break
            
            self._time = next_time
            await self._flush()

        self._time = end_time
        await self._flush()

    async def _flush(self):
        while True:
            next_time = self._get_next_scheduled_time()
            if not self.loop._ready and (next_time is None or next_time > self._time):
                break
                
            # yield control
            await asyncio.sleep(0)
    
    def _get_next_scheduled_time(self):
        try:
            return self.loop._scheduled[0]._when
        except IndexError:
            return None
