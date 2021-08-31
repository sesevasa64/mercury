import time
import qsilver

async def long_sleep():
    print("Hello")
    await qsilver.sleep(5)
    print("World")

async def test(coro):
    time.sleep(2.5)
    qsilver.cancel_coroutine(coro)
    time.sleep(2.5)

def main():
    qsilver.create_scheduler()

    coro = long_sleep()
    qsilver.add_coroutine(coro)
    qsilver.add_coroutine(test(coro))

    qsilver.run_forever()

if __name__ == "__main__":
    main()
