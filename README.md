# Mercury

Mercury is a tiny python library, which provides api to run multiply tasks concurrent in only one thread using async/await syntax. 

## Installation

You can install Mercury via pip:
```bash
pip intall mercury
```

## Usage

```python
import mercury

async def example():
    print("Hello")
    await mercury.sleep(1)
    print("World!")

mercury.create_scheduler()
mercury.add_coroutine(example())
mercury.run_forever()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
