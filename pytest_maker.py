import os
import ast
import yaml
import argparse
import importlib

from typing import Any, List, Tuple, Union


def print_imports(module_name: str) -> str:
    """
    Reads a Python module from a file and returns a string containing
    all the import statements found in the module.

    Args:
        module_name (str): The name of the module to be read.

    Returns:
        str: A string containing all the import statements found in
            the module.
    """
    with open(f'{module_name}.py', 'r') as f:
        source = f.read()

    imports = []
    for node in ast.iter_child_nodes(ast.parse(source)):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(f"import {name.name}")
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                if not node.module == 'typing':
                    imports.append(f"""from {node.module} import {
                        name.name + f'as {name.asname}'
                        if name.asname else name.name}""")
    return '\n'.join(imports)


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
        if test_name and '$' in test_name and 'fixture' not in test_name:
            func_name, val = test_name.split("$")
            func = getattr(module, func_name)
        elif 'fixture' in test_name:
            def fixture(): pass
            func, val = fixture, test_name.split("$")[1]
        else:
            print(test_name)
            return
        args = [test_data.get("args", '').replace("$", ", ")[2:] if test_data.get('args', None) else '']
        equals = test_data.get('equals', None)
        eval_equals = test_data.get('eval_equals', None)
        eval_less = test_data.get('eval_less', None)
        eval_lessoe = test_data.get('eval_lessoe', None)
        eval_more = test_data.get('eval_more', None)
        eval_moreoe = test_data.get('eval_moreoe', None)
        less = test_data.get('less', None)
        lessoe = test_data.get('lessoe', None)
        more = test_data.get('more', None)
        moreoe = test_data.get('moreoe', None)
        outtype = test_data.get('outtype', None)
        skip = test_data.get('skip', None)
        fail = test_data.get('fail', None)
        timeout = test_data.get('timeout', None)
        test_cases.append((
            func, args, equals, eval_equals, eval_less, eval_lessoe, eval_more,
            eval_moreoe, less, lessoe, more, moreoe, outtype, skip, fail, timeout,
            val))

    with open(f'test_{module_name}.py', 'w') as f:
        f.write('import pytest\n')
        f.write(print_imports(module_name) + '\n\n')
        f.write('from typing import *\n')
        f.write(f'from {module_name} import *\n\n\n')
        for i, (func, args, equals, eval_equals, eval_less, eval_lessoe, eval_more,
            eval_moreoe, less, lessoe, more, moreoe, outtype, skip, fail, timeout, 
                val) in enumerate(test_cases):
            arg_list = args[0]
            if skip:
                f.write('@pytest.mark.skip(\n')
                f.write(f'    reason="{skip}")\n')
            elif fail:
                f.write('@pytest.mark.xfail(\n')
                f.write(f'    reason="{fail}")\n')
            elif timeout:
                f.write(f'@pytest.mark.timeout({timeout})\n')
            if 'fixture' not in func.__name__:
                f.write(f'def test_{func.__name__}_{val}() -> None:\n' if 'fixture' not in arg_list
                        else f'def test_{func.__name__}_{val}(test_{arg_list}) -> None:\n' if arg_list[-1] != '*' else
                        f'def test_{func.__name__}_{val}(test_{arg_list[:-1]}) -> None:\n')
                f.write(f'    result = {func.__name__}({arg_list})\n' if 'fixture' not in arg_list
                        else f'    result = {func.__name__}(test_{arg_list})\n' if arg_list[-1] != '*' else
                        f'    result = {func.__name__}(*test_{arg_list[:-1]})\n')
                if outtype:
                    f.write(f'    assert isinstance(result, {outtype})\n')
                if equals:
                    f.write(f'    assert result == {repr(equals)}\n')
                if less:
                    f.write(f'    assert result < {repr(less)}\n')
                if lessoe:
                    f.write(f'    assert result <= {repr(lessoe)}\n')
                if more:
                    f.write(f'    assert result > {repr(more)}\n')
                if moreoe:
                    f.write(f'    assert result >= {repr(moreoe)}\n')
                if eval_equals:
                    f.write(f'    assert result == {repr(eval_equals)[1:-1]}\n')
                if eval_less:
                    f.write(f'    assert result < {repr(eval_less)[1:-1]}\n')
                if eval_lessoe:
                    f.write(f'    assert result <= {repr(eval_lessoe)[1:-1]}\n')
                if eval_more:
                    f.write(f'    assert result > {repr(eval_more)[1:-1]}\n')
                if eval_moreoe:
                    f.write(f'    assert result >= {repr(eval_moreoe)[1:-1]}\n')
                f.write("" if i == len(test_cases)-1 else "\n\n")
            else:
                f.write(f'@pytest.fixture\n')
                f.write(f'def test_{func.__name__}_{val}():\n')
                f.write(f'    return {arg_list}\n\n')
                
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
