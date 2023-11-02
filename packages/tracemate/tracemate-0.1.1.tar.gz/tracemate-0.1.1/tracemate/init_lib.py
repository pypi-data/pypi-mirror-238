# Creating the TraceMate library Python package structure
# The library will include functionalities for setting up logging and applying logging decorators to all functions in a module.

# Directory structure:
# tracemate/
# ├── __init__.py
# ├── logging_setup.py
# └── function_decorator.py

import os

tracemate_init_content = '''
# TraceMate Library
'''

tracemate_logging_setup_content = '''
import logging
from rich.console import Console

def setup_logging(log_file_name='tracemate_backend.log'):
    logging.basicConfig(filename=log_file_name, level=logging.INFO)
    backend_logger = logging.getLogger('backend')

    ui_logger = logging.getLogger('ui')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    ui_logger.addHandler(console_handler)

    console = Console()

    return backend_logger, ui_logger, console
'''

tracemate_function_decorator_content = '''
import inspect
import types
from functools import wraps

def logger_decorator(backend_logger, func):
    async def wrapper(*args, **kwargs):
        backend_logger.info(f"Entering {func.__name__}")
        result = await func(*args, **kwargs)
        backend_logger.info(f"Exiting {func.__name__}")
        return result
    return wrapper

def apply_decorator_to_all_functions_in_module(module, decorator):
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) or inspect.iscoroutinefunction(obj):
            setattr(module, name, decorator(obj))

def apply_logger_to_all_functions(backend_logger):
    current_module = types.ModuleType(__name__)
    for attr_name, attr_value in globals().items():
        if callable(attr_value):
            decorated_func = logger_decorator(backend_logger, attr_value)
            setattr(current_module, attr_name, decorated_func)
'''

# Save these files in the `/mnt/data/tracemate` directory
tracemate_dir = os.getcwd()
os.makedirs(tracemate_dir, exist_ok=True)

with open(f"{tracemate_dir}/__init__.py", "w") as f:
    f.write(tracemate_init_content)

with open(f"{tracemate_dir}/logging_setup.py", "w") as f:
    f.write(tracemate_logging_setup_content)

with open(f"{tracemate_dir}/function_decorator.py", "w") as f:
    f.write(tracemate_function_decorator_content)

tracemate_dir
