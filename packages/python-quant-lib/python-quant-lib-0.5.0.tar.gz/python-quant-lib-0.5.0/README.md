# PQL (Python Quant Lib)

PQL is a simple quantitative library written in Python and Python wrapped C++ using pybind11.
The original structure of that project is based on the [cmake pybind11 example](https://github.com/pybind/cmake_example).

The library is a personal project started to learn more about finance and therefore comes as is with no guarantees.

## Installation

Just clone this repository and pip install. Note the `--recursive` option which is
needed for the pybind11 submodule:

```bash
pip install pql
```

## Test call

```python
import datetime as dt
from pql.date import add_tenor

next_month = add_tenor(dt.date.today(), "1M")
print(next_month)
```


## License

This project is distributed under the MIT License

