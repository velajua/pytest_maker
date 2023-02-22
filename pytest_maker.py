import os
import yaml
import argparse
import importlib

from typing import Any, List, Tuple, Union


def generate_test_cases(module_name: str) -> None:
    """
    Generates pytest test cases from pytest_input.yaml
    for the given module.

    Args:
    module_name: Name of the module to generate test cases for.

    Returns:
    None.
    """
    if not os.path.isfile(f"{module_name}.py"):
        print(f"{module_name}.py does not exist.")
        return

    if not os.path.isfile("pytest_input.yaml"):
        print("pytest_input.yaml does not exist.")
        return

    with open('pytest_input.yaml', 'r') as f:
        data = yaml.safe_load(f)
    module = importlib.import_module(module_name)

    test_cases: List[Tuple[Any, List[str], Any, Union[type, None],
                           Union[str, None], Union[str, None], str]] = []
    for test_name, test_data in data.items():
        func_name, val = test_name.split("$")
        func = getattr(module, func_name)
        args = [test_data["args"].replace("$", ", ")[2:]]
        expected = test_data['expected']
        outtype = test_data.get('outtype', None)
        skip = test_data.get('skip', None)
        fail = test_data.get('fail', None)
        test_cases.append((
            func, args, expected, outtype, skip, fail, val))

    with open(f'test_{module_name}.py', 'w') as f:
        f.write('import pytest\n\n')
        f.write('from typing import *\n')
        f.write(f'from {module_name} import *\n\n\n')
        for i, (func, args, expected, outtype, skip, fail,
                val) in enumerate(test_cases):
            arg_list = args[0]
            if skip:
                f.write('@pytest.mark.skip(\n')
                f.write(f'    reason="{skip}")\n')
            if fail:
                f.write('@pytest.mark.xfail(\n')
                f.write(f'    reason="{fail}")\n')
            f.write(f'def test_{func.__name__}_{val}() -> None:\n')
            f.write(f'    result = {func.__name__}({arg_list})\n')
            if outtype:
                f.write(f'    assert isinstance(result, {outtype})\n')
            f.write(f'    assert result == {repr(expected)}')
            f.write("\n" if i == len(test_cases)-1 else "\n\n\n")
    while True:
        run_pytest = input("Do you want to run pytest? (y/n/all) ")
        if run_pytest.lower() in ['y', 'n', 'all']:
            break
        print("Invalid input. Please enter 'y', 'n', or 'all'.")

    if run_pytest.lower() == 'y':
        os.system(f"pytest test_{module_name}.py")
    elif run_pytest.lower() == 'all':
        os.system("pytest")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate pytest test cases from pytest_input.yaml')
    parser.add_argument(
        'module_name', type=str,
        help='Name of the module to generate test cases for')
    args = parser.parse_args()
    generate_test_cases(args.module_name)
