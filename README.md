# aiotime

An `asyncio` test helper that allows you to deterministically control the event loop's internal clock in your tests, affecting the behavior of the following functions:

1. `asyncio.sleep`
2. `loop.call_at`
3. `loop.call_later`

## Note about behavior

If you enter the `aiotime.FastForward` context manager (as in the `with` block in the examples below), then the `loop` supplied to its constructor will STOP triggering scheduled events, tasks or callbacks. Once you `__enter__` the context manager, you MUST call the returned object or the event loop will be stuck in time. Only when you `__exit__` the context manager will the loop return to normal behavior.

(Using the same event loop with and without `aiotime` control is not supported; there may be unexpected effects with scheduling at the margins.)

## Getting started

```python
# TODO Add to pypi
```

### Controlling `asyncio.sleep`

```python
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
```

### Controlling `loop.call_later`

```python
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
```