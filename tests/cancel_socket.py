import time
import qsilver

async def dummy(client, address):
    pass

async def test(listener):
    time.sleep(2)
    qsilver.cancel_coroutine(listener)

def main():
    qsilver.create_scheduler()

    server = qsilver.BasicTCPServer("localhost", 6969, 5)
    listener = server.listener(dummy)
    qsilver.add_coroutine(listener)
    qsilver.add_coroutine(test(listener))

    qsilver.run_forever()

if __name__ == "__main__":
    main()
