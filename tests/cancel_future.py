import time
import qsilver

def proceed():
    print("Hello")
    time.sleep(5)
    print("World")

async def helper():
    future = qsilver.AsyncFuture.from_pool(proceed)
    await future.result()

async def test(coro):
    time.sleep(2.5)
    qsilver.cancel_coroutine(coro)
    time.sleep(2.5)

def main():
    qsilver.create_scheduler()

    coro = helper()
    qsilver.add_coroutine(coro)
    qsilver.add_coroutine(test(coro))

    qsilver.run_forever()

if __name__ == "__main__":
    main()
