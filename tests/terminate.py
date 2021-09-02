import sys
import signal
import qsilver

async def dummy(client, address):
    pass

async def test():
    try:
        await qsilver.sleep(10)
    except qsilver.CancelCoroutine:
        print("Cancel!")
        await qsilver.sleep(1)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    qsilver.terminate()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    qsilver.create_scheduler()

    server = qsilver.BasicTCPServer("localhost", 6969, 5)
    listener = server.listener(dummy)
    qsilver.add_coroutine(listener)
    qsilver.add_coroutine(test())

    qsilver.run_forever()

if __name__ == "__main__":
    main()
