import inspect
import types
from functools import wraps

def logger_decorator(backend_logger, func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print("Before logging")  # Debugging line
            backend_logger.info(f"Entering {func.__name__}")
            print("After logging")  # Debugging line
            result = await func(*args, **kwargs)
            backend_logger.info(f"Exiting {func.__name__}")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            print("Before logging")  # Debugging line
            backend_logger.info(f"Entering {func.__name__}")
            print("After logging")  # Debugging line
            result = func(*args, **kwargs)
            backend_logger.info(f"Exiting {func.__name__}")
            return result
        return sync_wrapper

def apply_decorator_to_all_functions_in_module(module, backend_logger):
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) or inspect.iscoroutinefunction(obj):
            setattr(module, name, logger_decorator(backend_logger, obj))

# ... existing imports ...

def logger_decorator(backend_logger, func):
    print(f"Decorator being applied to {func.__name__}")  # Debugging line
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print("Entering async decorated function")  # Debugging line
            backend_logger.info(f"Entering {func.__name__}")
            result = await func(*args, **kwargs)
            backend_logger.info(f"Exiting {func.__name__}")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            print("Entering sync decorated function")  # Debugging line
            backend_logger.info(f"Entering {func.__name__}")
            result = func(*args, **kwargs)
            backend_logger.info(f"Exiting {func.__name__}")
            return result
        return sync_wrapper


# ... existing imports ...

def apply_logger_to_all_functions(backend_logger, functions_to_decorate):
    decorated_functions = {}
    for func in functions_to_decorate:
        decorated_func = logger_decorator(backend_logger, func)
        decorated_functions[func.__name__] = decorated_func
    return decorated_functions
