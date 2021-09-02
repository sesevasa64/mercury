import asyncio

async def t1():
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        while True:
            await asyncio.sleep(0)

async def t2(future: asyncio.Future):
    await asyncio.sleep(2)
    future.cancel()

async def main():
    t = t1()
    f1 = asyncio.ensure_future(t)
    f2 = asyncio.ensure_future(t2(t))
    await asyncio.gather(f1, f2)

asyncio.run(main())
