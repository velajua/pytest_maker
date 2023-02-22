# Automated Test Generation with YAML and Python
This repository provides a script for generating automated tests using a YAML input file and Python code. The script generates pytest test functions for each test case specified in the YAML file.

### Installation
To use this script, you'll need to install the required dependencies:

```python
pip install -r requirements.txt
```

### Usage
To use the test generator, create a YAML file with test cases and pass the name of the Python module to test as a command line argument when running the `pytest_maker.py` script:

```python
python pytest_maker.py my_module
```

This will generate a `test_my_module.py` file with pytest test functions.

### Example
As an example, let's say we have a module called `my_module.py` with the following functions:

```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def concat_str(a, b):
    return a + b

def concat_list(a, b):
    return a + b
```

### YAML Input File
The YAML input file should contain a dictionary with one key-value pair per test case. The key should be of the format <function_name>$<test_case_name>, where <function_name> is the name of the Python function to test and <test_case_name> is a descriptive name for the test case. The value should be a dictionary with keys beginning with "arg" representing the arguments to pass to the function and a "expected" key representing the expected output of the function. An optional "output_type" key can be used to specify the type of the expected output.

Here's an example input.yaml file:

```yaml
add$simple_add:
  args: $2$3
  expected: 5
  outtype: int
subtract$simple_subtract:
  args: $3$3
  expected: 0
  outtype: int
multiply$1:
  args: $1$7
  expected: 7
  outtype: int
```

Then, running `python pytest_maker.py my_module` will generate a file test_my_module.py with the following content which can then be run using the `pytest` library:

```python
import pytest

from typing import *
from my_module import *


def test_add_simple_add():
    result = add(2, 3)
    assert isinstance(result, int)
    assert result == 5


def test_subtract_simple_subtract():
    result = subtract(3, 3)
    assert isinstance(result, int)
    assert result == 0


def test_multiply_1():
    result = multiply(1, 7)
    assert isinstance(result, int)
    assert result == 7
```
