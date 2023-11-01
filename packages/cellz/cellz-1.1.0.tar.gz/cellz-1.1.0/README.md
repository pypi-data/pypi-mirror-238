# cellz

[![PyPI - Version](https://img.shields.io/pypi/v/cell.svg)](https://pypi.org/project/cell)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cell.svg)](https://pypi.org/project/cell)

## Installation

```console
pip install cellz
```

## Usage

Cellz is an interactive cell interpreter for python. It allows you to run python code from a source file, cell-by-cell: similar to the way we use cells in jupyter notebooks, and all from the command line.

Cellz is interactive: you can continue to develop the source code without leaving the interpreter!

First split you code into separate cells using the token '#%% cellname'

```python
#file.py
import sys

#%% cell1
print("hello!")

#%% cell2

def add1(x):
	return x+1
	
#%% cell3
print(add1(5))
```

Then run the file in the cellz interpreter

```
cellz file.py
```

This will start the interpreter, from which one can run specific cells of code, one at a time.  

## License

`cellz` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.