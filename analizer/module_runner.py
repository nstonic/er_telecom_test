import importlib
import os
from inspect import getmembers, isfunction
from typing import Callable

from django.conf import settings


class ModuleRunner(dict):
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._is_initialized:
            return

        super().__init__()
        app_name = settings.MODULES_APP_NAME
        modules_dir = settings.MODULES_DIR
        modules_list = os.listdir(settings.BASE_DIR / app_name / settings.MODULES_DIR)
        for module_name in modules_list:
            if not module_name.endswith('.py'):
                continue

            module_name, _ = module_name.rsplit('.', 1)
            module = importlib.import_module(f'{app_name}.{modules_dir}.{module_name}')
            self[module_name] = dict(getmembers(module, isfunction))

        self.__class__._is_initialized = True

    def run(self, data: dict) -> dict:
        function = self.get_function(data)
        return function(data)

    def get_function(self, data: dict) -> Callable:
        if not isinstance(data, dict):
            raise TypeError('Data must be dict')

        module_name = data.get('module')
        if not module_name:
            raise ValueError('Module not defined')
        module = self.get(module_name)
        if not module:
            raise ImportError(f'Unknown module {module_name}')

        function_name = data.get('function')
        if not function_name:
            raise ValueError('Function not defined')
        function = module.get(function_name)
        if not function:
            raise ImportError(f'Unknown function {function_name}')

        return function
