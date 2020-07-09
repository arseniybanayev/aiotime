import asyncio
import pytest
import datetime as dt
import aiotime

@pytest.mark.asyncio
async def test_asyncio_sleep():
    loop = asyncio.get_event_loop()

    # Try sleeping with normal loop behavior
    start = dt.datetime.now()
    sleep_task = asyncio.create_task(asyncio.sleep(0.25))
    await sleep_task
    assert dt.datetime.now() - start > dt.timedelta(seconds=0.25)

    with aiotime.FastForward(loop) as ff:
        # Try fast-forwarding through the sleep
        start = dt.datetime.now()
        sleep_task = asyncio.create_task(asyncio.sleep(0.25))
        await ff(1.5)  # ff more than necessary
        await sleep_task
        assert dt.datetime.now() - start < dt.timedelta(seconds=0.05)
    
    # Sleep with normal loop behavior now, after context manager exits
    start = dt.datetime.now()
    sleep_task = asyncio.create_task(asyncio.sleep(0.25))
    await sleep_task
    assert dt.datetime.now() - start > dt.timedelta(seconds=0.25)

@pytest.mark.asyncio
async def test_asyncio_call_later():
    loop = asyncio.get_event_loop()

    with aiotime.FastForward(loop) as ff:
        # Try call_later() with fast-forwarding
        start = dt.datetime.now()
        event = asyncio.Event()
        def test():
            event.set()
        loop.call_later(0.25, test)
        await ff(1.5)  # ff more than necessary
        await asyncio.wait_for(event.wait(), 2)  # timeout just in case
        assert dt.datetime.now() - start < dt.timedelta(seconds=0.05)
    
    # call_later() with normal loop behavior now, after context manager exits
    start = dt.datetime.now()
    event = asyncio.Event()
    def test():
        event.set()
    loop.call_later(0.25, test)
    await asyncio.wait_for(event.wait(), 1)  # timeout just in case
    assert dt.datetime.now() - start > dt.timedelta(seconds=0.25)