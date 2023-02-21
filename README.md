# Automated Test Generation with YAML and Python
This repository provides a script for generating automated tests using a YAML input file and Python code. The script generates pytest test functions for each test case specified in the YAML file.

### Installation
To use this script, you'll need to install the required dependencies:

```python
pip install -r requirements.txt
```

### Usage
To use the test generator, create a YAML file with test cases and pass the name of the Python module to test as a command line argument when running the test_maker.py script:

```python
python test_maker.py my_module
```

This will generate a test_my_module.py file with pytest test functions.

### Example
As an example, let's say we have a module called my_module with the following functions:

```python
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def divide(x, y):
    return x / y

def concat_str(a, b):
    return a + b

def concat_list(a, b):
    return a + b
```

### YAML Input File
The YAML input file should contain a dictionary with one key-value pair per test case. The key should be of the format function_name$test_case_name, where function_name is the name of the Python function to test and test_case_name is a descriptive name for the test case. The value should be a dictionary with keys beginning with "arg" representing the arguments to pass to the function and a "expected" key representing the expected output of the function. An optional "output_type" key can be used to specify the type of the expected output.

Here's an example input.yaml file:

```yaml
add$simple_add:
  arg1: 2
  arg2: 3
  expected: 5

subtract$simple_subtract:
  arg1: 3
  arg2: 3
  expected: 0
  output_type: int

divide$unit_divide:
  arg1: 3
  arg2: 3
  expected: 1
  output_type: float

divide$decimal_divide:
  arg1: 4
  arg2: 8
  expected: 0.5
  output_type: float

concat_str$simple_concat:
  arg1: 'hello'
  arg2: 'world'
  expected: 'helloworld'
  output_type: str

concat_list$add_list:
  arg1: [1, 2]
  arg2: [1, 2]
  expected: [1, 2, 1, 2]
  output_type: List
```

Then, running python test_maker.py my_module will generate a file test_my_module.py with the following content:

```python
import pytest

from typing import *
from my_module import *


def test_add_simple_add():
    result = add(2, 3)
    assert result == 5


def test_subtract_simple_subtract():
    result = subtract(3, 3)
    assert isinstance(result, int)
    assert result == 0


def test_divide_unit_divide():
    result = divide(3, 3)
    assert isinstance(result, float)
    assert result == 1


def test_divide_decimal_divide():
    result = divide(4, 8)
    assert isinstance(result, float)
    assert result == 0.5


def test_concat_str_simple_concat():
    result = concat_str('hello', 'world')
    assert isinstance(result, str)
    assert result == 'helloworld'


def test_concat_list_add_list():
    result = concat_list([1, 2], [1, 2])
    assert isinstance(result, List)
    assert result == [1, 2, 1, 2]
```
