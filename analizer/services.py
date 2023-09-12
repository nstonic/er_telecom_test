import importlib
from inspect import getmembers, isfunction, getdoc, getsource
from pathlib import Path
from typing import Callable

from django.conf import settings


def get_function(serialized_json: dict) -> Callable:
    if not isinstance(serialized_json, dict):
        raise TypeError('Data must be dict')

    module_name = serialized_json.get('module')
    if not module_name:
        raise ValueError('Module not defined')
    module_path = settings.MODULES_DIR.joinpath(module_name)
    module = importlib.import_module('.'.join(module_path.parts))
    members = dict(getmembers(module, isfunction))

    function_name = serialized_json.get('function')
    if not function_name:
        raise ValueError('Function not defined')

    try:
        function = members[function_name]
    except KeyError:
        raise ImportError(f'Unknown function {function_name}')

    return function


def collect_modules(dir_path: Path) -> dict:
    modules_list = dir_path.glob('*.py')

    modules = {}
    for module_path in modules_list:
        module_path_parts = list(module_path.parts)
        module_name = module_path_parts[-1].rsplit('.', 1)[0]
        module_path_parts[-1] = module_name

        module = importlib.import_module(
            '.'.join(module_path_parts)
        )
        functions = getmembers(module, isfunction)

        modules[module_name] = {}
        for function_name, function in functions:
            modules[module_name][function_name] = {
                'function_docs': getdoc(function),
                'function_source': getsource(function),
            }

    return modules
