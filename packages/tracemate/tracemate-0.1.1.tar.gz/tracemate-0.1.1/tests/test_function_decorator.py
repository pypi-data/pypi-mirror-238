import logging
import pytest
from unittest import mock
from ..tracemate.function_decorator import logger_decorator, apply_decorator_to_all_functions_in_module, apply_logger_to_all_functions
import types
import asyncio
import sys
import io

# Sample functions for testing
def sample_function(x, y):
    return x + y

async def async_sample_function(x, y):
    return x + y

# Mock module for testing
mock_module = types.ModuleType("mock_module")
setattr(mock_module, "sample_function", sample_function)
setattr(mock_module, "async_sample_function", async_sample_function)

def run_function(func, *args):
    if asyncio.iscoroutinefunction(func):
        asyncio.run(func(*args))
    else:
        func(*args)

def test_logger_decorator():
    with mock.patch('logging.Logger') as MockLogger:
        backend_logger = MockLogger()
        decorated_func = logger_decorator(backend_logger, sample_function)
        run_function(decorated_func, 1, 2)
        backend_logger.info.assert_any_call("Entering sample_function")
        backend_logger.info.assert_any_call("Exiting sample_function")

def test_apply_decorator_to_all_functions_in_module():
    with mock.patch('logging.Logger') as MockLogger:
        backend_logger = MockLogger()
        apply_decorator_to_all_functions_in_module(mock_module, backend_logger)
        run_function(mock_module.sample_function, 1, 2)
        run_function(mock_module.async_sample_function, 1, 2)
        backend_logger.info.assert_any_call("Entering sample_function")
        backend_logger.info.assert_any_call("Exiting sample_function")

def run_function(func, *args):
    if asyncio.iscoroutinefunction(func):
        asyncio.run(func(*args))
    else:
        func(*args)

def test_apply_logger_to_all_functions():
    log_stream = io.StringIO()

    # Explicitly configure logging
    logging.basicConfig(stream=log_stream, level=logging.INFO)

    # Create a unique logger for this test
    backend_logger = logging.getLogger('backend_test_unique')
    backend_logger.setLevel(logging.INFO)
    backend_logger.propagate = False

    # Debug: Check if the logger has any handlers
    print(f"Handlers before adding: {backend_logger.handlers}")

    # Attach the StreamHandler to the logger
    handler = logging.StreamHandler(log_stream)
    backend_logger.addHandler(handler)

    # Debug: Check if the logger has the correct handler now
    print(f"Handlers after adding: {backend_logger.handlers}")

    functions_to_decorate = [sample_function, async_sample_function]
    decorated_functions = apply_logger_to_all_functions(backend_logger, functions_to_decorate)
    backend_logger.info("This is a test log entry")

    run_function(decorated_functions['sample_function'], 1, 2)
    run_function(decorated_functions['async_sample_function'], 1, 2)

    log_stream.flush()  # Ensure all data gets written to the stream

    log_contents = log_stream.getvalue()

    # Debug: Print the captured logs
    print(log_contents)

    assert "This is a test log entry" in log_contents
    assert "Entering sample_function" in log_contents
