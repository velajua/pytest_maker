import sys
import yaml
import importlib

from typing import *


def generate_test_cases(module_name):
    with open('input.yaml', 'r') as f:
        data = yaml.safe_load(f)
    module = importlib.import_module(module_name)

    test_cases = []
    for test_name, test_data in data.items():
        func_name, val = test_name.split("$")
        func = getattr(module, func_name)
        args = [test_data[arg_name] for arg_name in test_data if arg_name.startswith('arg')]
        expected = test_data['expected']
        output_type = test_data.get('output_type', None)
        test_cases.append((func, args, expected, output_type, val))

    with open(f'test_{module_name}.py', 'w') as f:
        f.write(f'import pytest\n\n')
        f.write('from typing import *\n')
        f.write(f'from {module_name} import *\n\n\n')
        for i, (func, args, expected, output_type, val) in enumerate(test_cases):
            arg_list = ', '.join(map(repr, args))
            f.write(f'def test_{func.__name__}_{val}():\n')
            f.write(f'    result = {func.__name__}({arg_list})\n')
            if output_type:
                f.write(f'    assert isinstance(result, {output_type})\n')
            f.write(f'    assert result == {repr(expected)}')
            f.write("\n" if i == len(test_cases)-1 else "\n\n\n")


if __name__ == '__main__':
    module_name = sys.argv[1]
    generate_test_cases(module_name)
