# QSilver

QSilver is a tiny python library, which provides api to run multiply tasks concurrent in only one thread using async/await syntax. 

## Installation

You can install QSilver via pip:
```bash
pip intall qsilver
```

## Usage

```python
import qsilver

async def example():
    print("Hello")
    await qsilver.sleep(1)
    print("World!")

qsilver.create_scheduler()
qsilver.add_coroutine(example())
qsilver.run_forever()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
